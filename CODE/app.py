from datetime import datetime
from typing import Optional

from flask import Flask, jsonify, render_template, request, url_for
from flask_cors import CORS

from cryptopunks_data_pipeline.data_preparation_pipeline import (
    create_spark_session,
    run_pipeline,
)
from GridSearch.indicators_search_v2 import run_logic
from QLearnerModel.strategy_evaluation.money_machine import main

app = Flask(__name__)
cors = CORS(app)
spark = create_spark_session()


def validate_config(config: dict) -> Optional[dict]:
    """Returns None of no issues with validating the config"""
    training_sd = datetime.strptime(config.get("training_sd"), "%Y-%m-%d")
    training_ed = datetime.strptime(config.get("training_ed"), "%Y-%m-%d")
    test_sd = datetime.strptime(config.get("test_sd"), "%Y-%m-%d")
    test_ed = datetime.strptime(config.get("test_ed"), "%Y-%m-%d")

    # validate training and testing dates
    if not training_sd < training_ed:
        return {"Error": "Training Start Date must be before than Training End Date."}
    if not test_sd < test_ed:
        return {"Error": "Testing Start Date must be before than Testing End Date."}
    if not training_ed < test_sd:
        return {"Error": "Training End Date must be before than Testing Start Date."}


@app.route("/")
def index() -> str:
    example_embed = "CSE-6242: Cryptopunks Project Flask API"
    return render_template("index.html", embed=example_embed)


@app.route("/run_qlearner")
def run_qlearner() -> dict:
    config = request.args.to_dict()
    validation = validate_config(config)
    if validation:
        return validation

    print(f"running pipeline using config: {config}")
    input_df = run_pipeline(spark, **config)
    print(input_df)
    output_df = main(config=config, dataframebtc=input_df)

    return jsonify(output_df.fillna(0).to_dict("records"))


@app.route("/run_gridsearch")
def run_gridsearch() -> dict:
    config = request.args.to_dict()
    validation = validate_config(config)
    if validation:
        return validation

    print(f"running pipeline using config: {config}")
    input_df = run_pipeline(spark, **config)
    print(input_df)
    output_df = run_logic(config=config, dataframebtc_input=input_df)

    return jsonify(output_df.fillna(0).to_dict("records"))


"""
1) To Run the Flask App locally outside of Docker, run this script `python app.py`
2) To test Flask is running, go to following URL in your browser: http://127.0.0.1:5001
3) To trigger the Q-learner, go to the URL printed on the console output
"""
if __name__ == "__main__":
    config_dict = {
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

    with app.test_request_context():

        # Q-Learner Method
        qlearner_url = url_for("run_qlearner", **config_dict)
        print("OBTAIN Q-LEAERNER RESPONSE AT THIS URL:")
        print(f"http://127.0.0.1:5001{qlearner_url}")
        gridsearch_url = url_for("run_gridsearch", **config_dict)
        print("OBTAIN GRIDSEARCH RESPONSE AT THIS URL:")
        print(f"http://127.0.0.1:5001{gridsearch_url}")
        app.run(debug=True, host="0.0.0.0", port=5001)
