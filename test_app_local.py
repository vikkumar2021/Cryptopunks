from cryptopunks_data_pipeline.data_preparation_pipeline import (
    create_spark_session,
    run_pipeline,
)
from QLearnerModel.strategy_evaluation.money_machine import main
from GridSearch.indicators_search_v2 import run_logic


spark = create_spark_session()


if __name__ == "__main__":
    config = {
        "ticker": "BTC",
        "training_sd": "2017-05-01",
        "training_ed": "2018-05-01",
        "test_sd": "2018-05-02",
        "test_ed": "2022-02-01",
        "sv": 500000,
        "sma_window": 14,
        "bollinger_window": 14,
        "bollinger_stdvs": 3,
        "so_window": 14,
        "so_window_sma": 14,
        "obv": False,
        "macd": True,
        "include_sentiment": False,
        "mom_window": 14,
        "alpha": 0.1,
        "gamma": 0.9,
        "rar": 0.99,
        "radr": 0.8,
        "sma_threshold": 0.2,
        "so_ul": 80,
        "so_ll": 20,
        "mom_threshold": 0.2,
        "sentiment_threshold": 0.3,
    }
    print(f"running pipeline using config: {config}")
    input_df = run_pipeline(spark, **config)
    print(input_df)
    #output_df = main(config=config, dataframebtc=input_df)
    output_df = run_logic(config=config, dataframebtc_input=input_df)
    print(output_df)