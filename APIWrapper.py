from flask import Flask, request, jsonify, url_for
from cryptopunks_data_pipeline.data_preparation_pipeline import run_pipeline
from cryptopunks_data_pipeline.data_preparation_pipeline import create_spark_session
from QLearnerModel.strategy_evaluation.money_machine import main


app = Flask(__name__)
spark = create_spark_session()


@app.route('/')
def index():
    return 'CSE-6242: Cryptopunks Project Flask API'


@app.route("/run_qlearner")
def run_qlearner():
    config = request.args.to_dict()
    print(f'running pipeline using config: {config}')
    input_df = run_pipeline(spark, **config)
    print(input_df)
    output_df = main(config=config, dataframebtc=input_df)

    return output_df.to_dict()


'''
1) To Run the Flask App, simply run the file
2) On your Local Browser go to following home page: http://127.0.0.1:5000 
3) To view parameters being passed, go to following page:
http://127.0.0.1:5000/run_qlearner?sma_window=14&bollinger_window=20&bollinger_stdvs=2&so_window=14&so_window_sma=3&obv=True&mom_window=14
'''
if __name__ == '__main__':
    with app.test_request_context():
        url2 = url_for('run_qlearner',
                       training_sd='2017-01-01',
                       training_ed='2018-12-31',
                       test_sd='2019-01-01',
                       test_ed='2019-12-31',
                       sma_window='14',
                       bollinger_band_sma='20',
                       bollinger_band_stdev='2',
                       so_window='14',
                       so_window_sma='3',
                       obv='True',
                       mom_window='14',
                       # sentiment_threshold=0.3,
                       sv=1000000)
        print(url2)
    app.run(debug=True)
