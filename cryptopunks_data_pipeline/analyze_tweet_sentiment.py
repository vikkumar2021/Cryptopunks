from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F
from pyspark.sql import DataFrame as SparkDataFrame
from nltk.sentiment import SentimentIntensityAnalyzer
import json


def read_tweets_data(spark: SparkSession, file_path: str) -> SparkDataFrame:
    """Read raw tweets CSV file"""

    schema = StructType(
        [
            StructField("id", StringType(), True),
            StructField("user", StringType(), True),
            StructField("fullname", StringType(), True),
            StructField("url", StringType(), True),
            StructField("timestamp", TimestampType(), True),
            StructField("replies", StringType(), True),
            StructField("likes", LongType(), True),
            StructField("retweets", LongType(), True),
            StructField("text", StringType(), True),
        ]
    )
    tweets_df = spark.read.option("delimiter", ";").csv(
        file_path, header=True, schema=schema
    )

    # TODO: Remove Limit on Dataframe when running on cluster
    tweets_df_subset = tweets_df  # .limit(50000)

    return tweets_df_subset.withColumnRenamed("timestamp", "tweet_timestamp").where(
        "text IS NOT NULL"
    )


def analyze_tweet_sentiment(tweets_df: SparkDataFrame) -> SparkDataFrame:
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
    return (
        tweets_df.withColumn("tweets_analyzed", sentiment_udf("text"))
        .select(
            "*",
            F.get_json_object("tweets_analyzed", "$.neg")
            .cast(DecimalType(4, 3))
            .alias("negative"),
            F.get_json_object("tweets_analyzed", "$.neu")
            .cast(DecimalType(4, 3))
            .alias("neutral"),
            F.get_json_object("tweets_analyzed", "$.pos")
            .cast(DecimalType(4, 3))
            .alias("positive"),
            F.get_json_object("tweets_analyzed", "$.compound")
            .cast(DecimalType(4, 3))
            .alias("compound"),
        )
        .where("neutral != 1.0")
    )


def aggregate_tweet_sentiment(df: SparkDataFrame) -> SparkDataFrame:
    """Aggregate sentiment data from individual tweets to a daily level of granularity"""

    df.createOrReplaceTempView("tweet_sentiment_unagg")
    df_agg = spark.sql(
        """
    WITH tweet_sentiment_labaled AS
        (SELECT
            CAST(tweet_timestamp AS Date) AS tweet_date,
            compound,
            CASE
                WHEN negative > positive
                    AND negative > neutral
                    THEN 'negative'
                WHEN positive > negative
                    AND positive > neutral
                    THEN 'positive'
                WHEN neutral > positive
                    AND neutral > negative
                    THEN 'neutral'
                END AS overall_sentiment
        FROM
            tweet_sentiment_unagg)
    
    SELECT
        tweet_date,
        AVG(CASE WHEN overall_sentiment = 'positive' THEN 1 ELSE 0 END) AS pct_positive,
        AVG(CASE WHEN overall_sentiment = 'negative' THEN 1 ELSE 0 END) AS pct_negative,
        AVG(CASE WHEN overall_sentiment = 'neutral' THEN 1 ELSE 0 END) AS pct_neutral,
        AVG(compound) AS avg_compound_sentiment,
        COUNT(*) AS tweet_volume
    FROM
        tweet_sentiment_labaled
    GROUP BY tweet_date
    """
    )

    return df_agg


def save_tweets(spark: SparkSession, file_path: str) -> None:
    df_tweets = read_tweets_data(spark, file_path)
    print(df_tweets.count())
    df_sentiment = analyze_tweet_sentiment(df_tweets)
    df_sentiment.printSchema()
    df_agg_sentiment = aggregate_tweet_sentiment(df_sentiment)
    df_agg_sentiment.write.csv("aggregated_tweet_sentiment.csv", header=True)

    return df_agg_sentiment
