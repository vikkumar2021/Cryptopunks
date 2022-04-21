from flask import Flask, request, url_for, render_template, jsonify
from flask_cors import CORS

from cryptopunks_data_pipeline.data_preparation_pipeline import (
    create_spark_session,
    run_pipeline,
)
from QLearnerModel.strategy_evaluation.money_machine import main
from GridSearch.indicators_search_v2 import run_logic


app = Flask(__name__)
cors = CORS(app)
spark = create_spark_session()


@app.route("/")
def index() -> str:
    example_embed = "CSE-6242: Cryptopunks Project Flask API"
    return render_template("index.html", embed=example_embed)


@app.route("/d3_test")
def d3_test() -> str:
    example_embed = "Test D3"
    return render_template("interactive.html", embed=example_embed)


@app.route("/run_qlearner")
def run_qlearner() -> dict:
    config = request.args.to_dict()
    print(f"running pipeline using config: {config}")
    input_df = run_pipeline(spark, **config)
    print(input_df)
    output_df = main(config=config, dataframebtc=input_df)

    return jsonify(output_df.fillna(0).to_dict('records'))


@app.route("/run_gridsearch")
def run_gridsearch() -> dict:
    config = request.args.to_dict()
    print(f"running pipeline using config: {config}")
    input_df = run_pipeline(spark, **config)
    print(input_df)
    output_df = run_logic(config=config, dataframebtc_input=input_df)

    return jsonify(output_df.fillna(0).to_dict())


"""
1) To Run the Flask App, run this script
2) To test Flask is running, go to following URL in your browser: http://127.0.0.1:5000
3) To trigger the Q-learner, go to the URL printed on the console output
"""
if __name__ == "__main__":
    config_dict = {
        "ticker": "BTC",
        "training_sd": "2017-05-01",
        "training_ed": "2018-05-01",
        "test_sd": "2018-05-02",
        "test_ed": "2019-02-01",
        "sv": 500000,
        "sma_window": 14,
        "bollinger_band_sma": 14,
        "bollinger_band_stdev": 3,
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
        url2 = url_for("run_qlearner", **config_dict)
        print("TRIGGER Q-LEAERNER BY CLICKING THIS URL:")
        print(f"http://127.0.0.1:5000/{url2}")
    app.run(debug=True, host="0.0.0.0", port=5000)
