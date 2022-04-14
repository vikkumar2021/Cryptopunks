from typing import Optional
from pandas import DataFrame as PandasDataFrame
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession
from analyze_tweet_sentiment import save_tweets
import os

CWD = os.path.dirname(os.path.abspath(__file__))
PRICE_FILE_PATH = os.path.join(CWD, "BTC-USD_2017-2022.csv")
TWEETS_FILE_PATH = os.path.join(CWD, "aggregated_tweet_sentiment.csv")


def create_spark_session():
    """Create Spark Session"""

    return (
        SparkSession.builder.appName("test")
        .master("local[*]")
        .enableHiveSupport()
        .getOrCreate()
    )


def read_stock_price_data(spark: SparkSession) -> SparkDataFrame:
    """Read stock price CSV file from Yahoo Finance"""

    schema = StructType(
        [
            StructField("Date", TimestampType(), True),
            StructField("Open", DecimalType(10, 2), True),
            StructField("High", DecimalType(10, 2), True),
            StructField("Low", DecimalType(10, 2), True),
            StructField("Close", DecimalType(10, 2), True),
            StructField("Adj Close", DecimalType(10, 2), True),
            StructField("Volume", LongType(), True),
        ]
    )
    df = (
        spark.read.csv(PRICE_FILE_PATH, header=True, schema=schema)
        .withColumnRenamed("Adj Close", "Adj_Close")
        .withColumnRenamed("Date", "TradeDate")
        .withColumn("Ticker", F.lit("BTC"))
    )

    return df


def read_aggregated_tweets(spark: SparkSession) -> SparkDataFrame:
    """Read aggregated tweets data (if it already exists)"""
    schema = StructType(
        [
            StructField("tweet_date", StringType(), True),
            StructField("pct_positive", FloatType(), True),
            StructField("pct_negative", FloatType(), True),
            StructField("pct_neutral", FloatType(), True),
            StructField("avg_compound_sentiment", FloatType(), True),
            StructField("tweet_volume", LongType(), True),
        ]
    )

    return spark.read.csv(TWEETS_FILE_PATH, header=True, schema=schema)


def add_price_to_SMA_ratio(
    spark: SparkSession, df: SparkDataFrame, sma_window: int
) -> SparkDataFrame:
    """Add price to simple moving average ratio"""

    df.createOrReplaceTempView("add_price_to_SMA_ratio")
    df_transformed = spark.sql(
        f"""
        WITH cte1 AS
            (SELECT
            *,
            AVG(Adj_Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {sma_window} DAYS PRECEDING AND CURRENT ROW) AS rolling_avg
            FROM add_price_to_SMA_ratio)

        SELECT
        *,
        ((Close / rolling_avg) - 1) AS price_to_SMA_ratio
        FROM cte1
        """
    )

    return df_transformed


def add_bollinger_bands(
    spark: SparkSession, df: SparkDataFrame, bollinger_window: int, bollinger_stdvs: int
) -> SparkDataFrame:
    """Add Bollinger Bands to dataframe"""

    df.createOrReplaceTempView("add_bollinger_bands")
    df_transformed = spark.sql(
        f"""
        WITH cte1 AS
            (SELECT
            *,
            AVG(Adj_Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {bollinger_window} DAYS PRECEDING AND CURRENT ROW) AS bollinger_sma,
            STDDEV(Adj_Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {bollinger_window} DAYS PRECEDING AND CURRENT ROW) AS bollinger_rolling_std
            FROM add_bollinger_bands),
        cte2 AS (
            SELECT
            *,
            (bollinger_sma - (bollinger_rolling_std * {bollinger_stdvs})) AS bollinger_band_lower,
            (bollinger_sma + (bollinger_rolling_std * {bollinger_stdvs})) AS bollinger_band_upper
            FROM cte1
        )

        SELECT
            *,
            (Adj_Close - bollinger_band_lower)/(bollinger_band_upper - bollinger_band_lower) AS bollinger_band_percentage
        FROM
        cte2
        """
    )

    return df_transformed.drop("bollinger_rolling_std")


def add_stochastic_oscillator(
    spark: SparkSession, df: SparkDataFrame, so_window: int, so_window_sma: int
) -> SparkDataFrame:
    df.createOrReplaceTempView("add_stochastic_oscillator")
    df_transformed = spark.sql(
        f"""
        WITH cte1 AS
            (SELECT
            *,
            MAX(Adj_Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {so_window} DAYS PRECEDING AND CURRENT ROW) AS max_window_price,
            MIN(Adj_Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {so_window} DAYS PRECEDING AND CURRENT ROW) AS min_window_price
            FROM add_stochastic_oscillator),
        cte2 AS (SELECT
        *,
        (Adj_Close - min_window_price)/(max_window_price - min_window_price) * 100.0 AS stochastic_oscillator
        FROM cte1)

        SELECT
        *,
        AVG(stochastic_oscillator) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL {so_window_sma} DAYS PRECEDING AND CURRENT ROW) AS stochastic_oscillator_sma
        FROM
        cte2
        """
    )

    return (
        df_transformed.drop("max_window_price")
        .drop("min_window_price")
        .drop("stochastic_oscillator")
    )


def add_on_balance_volume(spark: SparkSession, df: SparkDataFrame) -> SparkDataFrame:
    """
    Add On Balance Volume
    https://www.investopedia.com/terms/o/onbalancevolume.asp
    """

    df.createOrReplaceTempView("add_on_balance_volume")
    df_transformed = spark.sql(
        """
        WITH cte1 AS
        (SELECT *,
                CASE
                    WHEN (Adj_Close - Open) > 0 THEN 1
                    WHEN (Adj_Close - Open) < 0 THEN -1
                    ELSE 0 END AS multiplier
        FROM
            add_on_balance_volume)

        SELECT
            *,
            SUM(Volume * multiplier) OVER(PARTITION BY Ticker ORDER BY TradeDate ASC) AS on_balance_volume
        FROM
            cte1
        """
    )

    return df_transformed


def add_momentum(spark: SparkSession, df: SparkDataFrame, mom_window) -> SparkDataFrame:
    """
    Add Momentum
    """

    df.createOrReplaceTempView("add_momentum")
    df_transformed = spark.sql(
        f"""
        WITH cte1 AS
        (SELECT *,
                FIRST(Adj_Close) OVER(
                    PARTITION BY Ticker
                    ORDER BY TradeDate ASC
                    RANGE BETWEEN INTERVAL {mom_window} DAYS PRECEDING AND CURRENT ROW) AS window_start_price,
                LAST(Adj_Close) OVER(
                    PARTITION BY Ticker
                    ORDER BY TradeDate ASC
                    RANGE BETWEEN INTERVAL {mom_window} DAYS PRECEDING AND CURRENT ROW) AS window_end_price
        FROM
            add_momentum)

        SELECT
            *,
            (window_end_price/window_start_price) - 1 AS momentum
        FROM
            cte1
        """
    )

    return df_transformed  # .drop('window_start_price').drop('window_end_price')


def add_MACD(df: PandasDataFrame) -> PandasDataFrame:
    """Moving Average Convergence Divergence"""

    price_col = "Adj_Close"
    df["MACD_raw"] = (
        df[[price_col]].ewm(span=12).mean() - df[[price_col]].ewm(span=26).mean()
    )
    df["MACD_signal"] = df[["MACD_raw"]].ewm(span=9).mean()
    df["MACD"] = df["MACD_raw"] - df["MACD_signal"]
    df.drop(columns=["MACD_raw", "MACD_signal"])

    return df


def run_pipeline(
    spark: SparkSession,
    sma_window: Optional[int] = None,
    bollinger_window: Optional[int] = None,
    bollinger_stdvs: Optional[int] = None,
    so_window: Optional[int] = None,
    so_window_sma: Optional[int] = None,
    obv: Optional[bool] = None,
    macd: Optional[bool] = None,
    mom_window: Optional[int] = None,
    include_sentiment: Optional[bool] = None,
) -> PandasDataFrame:
    """Run data preparation pipeline."""
    df_price = read_stock_price_data(spark)

    # the following parameters must all be passed if either is present
    if any([bollinger_window, bollinger_stdvs]):
        assert all([bollinger_window, bollinger_stdvs])
        df_price = add_bollinger_bands(
            spark, df_price, bollinger_window, bollinger_stdvs
        )
    if any([so_window, so_window_sma]):
        assert all([so_window, so_window_sma])
        df_price = add_stochastic_oscillator(spark, df_price, so_window, so_window_sma)

    # transform price data to add indicators
    if sma_window:
        df_price = add_price_to_SMA_ratio(spark, df_price, sma_window)
    if obv:
        df_price = add_on_balance_volume(spark, df_price)
    if mom_window:
        df_price = add_momentum(spark, df_price, mom_window)

    if include_sentiment:
        # Use aggregated version of the tweets data if it exists, otherwise recompute it
        if os.path.exists(TWEETS_FILE_PATH):
            df_agg_sentiment = read_aggregated_tweets(spark)
        else:
            df_agg_sentiment = save_tweets(
                spark, "/Users/salmanmukhi/Downloads/BTC_tweets.csv"
            )
        df_joined = df_price.join(
            df_agg_sentiment, df_price.TradeDate == df_agg_sentiment.tweet_date, "inner"
        )
    else:
        df_joined = df_price

    pandas_df = df_joined.toPandas().sort_values(by=["TradeDate"])
    if macd:
        pandas_df = add_MACD(pandas_df)
    #print(pandas_df)
    pandas_df.to_csv(os.path.join(CWD, "pipeline_export.csv"))

    return pandas_df


if __name__ == "__main__":
    spark = create_spark_session()
    run_pipeline(
        spark,
        sma_window=14,
        bollinger_window=20,
        bollinger_stdvs=2,
        so_window=14,
        so_window_sma=3,
        obv=True,
        mom_window=14,
        macd=True,
        include_sentiment=True,
    )
