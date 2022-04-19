import json

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import (DecimalType, DoubleType, LongType, MapType,
                               StringType, StructField, StructType,
                               TimestampType)

PRICE_FILE_PATH = '/Users/salmanmukhi/Downloads/BTC-USD_2017-2022.csv'
TWEETS_FILE_PATH = '/Users/salmanmukhi/Downloads/BTC_tweets.csv'


def create_spark_session():
    """Create Spark Session"""

    return (SparkSession
            .builder
            .appName('test')
            .master("local[*]")
            .enableHiveSupport()
            .getOrCreate()
           )


def read_stock_price_data(spark: SparkSession, file_path: str) -> DataFrame:
    """Read stock price CSV file from Yahoo Finance"""

    schema = StructType([
        StructField("Date", TimestampType(), True),
        StructField("Open", DecimalType(10,2), True),
        StructField("High", DecimalType(10,2), True),
        StructField("Low", DecimalType(10,2), True),
        StructField("Close", DecimalType(10,2), True),
        StructField("Adj Close", DecimalType(10,2), True),
        StructField("Volume", LongType(), True),
    ])
    df = (spark.read.csv(PRICE_FILE_PATH, header=True, schema=schema)
        .withColumnRenamed("Adj Close", "Adj_Close")
        .withColumnRenamed("Date", "TradeDate")
        .withColumn("Ticker", F.lit("BTC"))
        )

    return df


def read_tweets_data(spark: SparkSession, file_path: str) -> DataFrame:
    """Read raw tweets CSV file"""

    schema = StructType([
        StructField("id",StringType(),True),
        StructField("user",StringType(),True),
        StructField("fullname",StringType(),True),
        StructField("url",StringType(),True),
        StructField("timestamp",TimestampType(),True),
        StructField("replies",StringType(),True),
        StructField("likes",LongType(),True),
        StructField("retweets",LongType(),True),
        StructField("text",StringType(),True)]
    )
    tweets_df = (spark
        .read
        .option('delimiter', ';')
        .csv(file_path, header=True, schema=schema))
    
    # TODO: Remove Limit on Dataframe when running on cluster
    tweets_df_subset = tweets_df.limit(50000)

    return (tweets_df_subset
        .withColumnRenamed("timestamp", "tweet_timestamp")
        .where('text IS NOT NULL'))


def transform_stock_price_data(df: DataFrame) -> DataFrame:
    """Add rolling averages and Bollinger Bands to dataframe"""

    df.createOrReplaceTempView('btc')
    df_transformed = spark.sql("""
        WITH btc_transform1 AS
            (SELECT
            *,
            AVG(Open) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL 7 DAYS PRECEDING AND CURRENT ROW) AS rolling_7_day_avg,
            AVG(Open) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL 200 DAYS PRECEDING AND CURRENT ROW) AS rolling_200_day_avg,
            AVG(Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL 200 DAYS PRECEDING AND CURRENT ROW) AS rolling_20_day_avg,
            STDDEV(Close) OVER(
                PARTITION BY Ticker
                ORDER BY TradeDate ASC
                RANGE BETWEEN INTERVAL 200 DAYS PRECEDING AND CURRENT ROW) AS rolling_20_day_std
            FROM btc)

        SELECT
        *,
        (rolling_20_day_avg - rolling_20_day_std) AS bollinger_band_lower,
        (rolling_20_day_avg + rolling_20_day_std) AS bollinger_band_upper
        FROM btc_transform1
        """)
    
    return df_transformed


def analyze_tweet_sentiment(tweets_df: DataFrame) -> DataFrame:
    """
        Use NLTK's pretrained SentimentIntensityAnalyzer to measure the sentiment
        of each tweet. Filter out tweets such as those in different languages that will default to a score
        of neutral=1.0.
    """
    
    sia = SentimentIntensityAnalyzer()

    # Wrap function in UDF
    def get_tweet_sentiment(tweet: str) -> str:
        sentiment_score = sia.polarity_scores(tweet)
        return json.dumps(sentiment_score)

    sentiment_udf = F.udf(get_tweet_sentiment, StringType())
    # sentiment_udf = F.udf(get_tweet_sentiment, MapType(StringType(), DoubleType()))
    return (tweets_df
        .withColumn('tweets_analyzed', sentiment_udf('text'))
        .select("*",
            F.get_json_object('tweets_analyzed', '$.neg').cast(DecimalType(4,3)).alias('negative'),
            F.get_json_object('tweets_analyzed', '$.neu').cast(DecimalType(4,3)).alias('neutral'),
            F.get_json_object('tweets_analyzed', '$.pos').cast(DecimalType(4,3)).alias('positive'),
            F.get_json_object('tweets_analyzed', '$.compound').cast(DecimalType(4,3)).alias('compound')
        )
        .where('neutral != aa1.0')
    )


def aggregate_tweet_sentiment(df):
    """Aggregate sentiment data from individual tweets to a daily level of granularity"""

    df.createOrReplaceTempView('tweet_sentiment_unagg')
    df_agg = spark.sql("""
    WITH tweet_sentiment_labaled AS
        (SELECT CAST(tweet_timestamp AS Date) AS tweet_date,
            CASE
                WHEN compound <= -0.05
                    THEN 'negative'
                WHEN positive >= 0.05
                    THEN 'positive'
                WHEN compound > -0.05
                    AND compound < 0.05 
                    THEN 'neutral'
                END AS overall_sentiment
        FROM
            tweet_sentiment_unagg)
    
    SELECT
        tweet_date,
        AVG(CASE WHEN overall_sentiment = 'positive' THEN 1 ELSE 0 END) AS pct_positive,
        AVG(CASE WHEN overall_sentiment = 'negative' THEN 1 ELSE 0 END) AS pct_negative,
        AVG(CASE WHEN overall_sentiment = 'neutral' THEN 1 ELSE 0 END) AS pct_neutral,
        COUNT(*) AS tweet_volume
    FROM
        tweet_sentiment_labaled
    GROUP BY tweet_date
    """)
    
    return df_agg



if __name__ == "__main__":
    spark = create_spark_session()
    df_price_raw = read_stock_price_data(spark, PRICE_FILE_PATH)
    df_price = transform_stock_price_data(df_price_raw)
    price_cols = ["TradeDate",
                  "rolling_20_day_avg",
                  "bollinger_band_lower",
                  "bollinger_band_upper"]
    df_price.select(price_cols).show()
    df_tweets = read_tweets_data(spark, TWEETS_FILE_PATH)
    df_sentiment = analyze_tweet_sentiment(df_tweets)
    df_sentiment.printSchema()
    tweet_cols = ['tweet_timestamp',
                  'likes',
                  'retweets',
                  'negative',
                  'positive',
                  'neutral',
                  'compound']
    df_sentiment.select(tweet_cols).show()
    df_agg_sentiment = aggregate_tweet_sentiment(df_sentiment)
    df_agg_sentiment.show()
    
    df_joined = df_price.join(df_agg_sentiment, df_price.TradeDate == df_agg_sentiment.tweet_date, 'inner')
    df_joined.show()