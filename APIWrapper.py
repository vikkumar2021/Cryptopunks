from flask import Flask, request, jsonify, url_for
from cryptopunks_data_pipeline.data_preparation_pipeline import run_pipeline_helper

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'


@app.route("/indicators")
def indicators():
    ticker = request.args.get('ticker', 'Error: Argument not Found')
    training_sd = request.args.get('training_sd', 'Error: Argument not Found')
    training_ed = request.args.get('training_ed', 'Error: Argument not Found')
    test_sd = request.args.get('test_sd', 'Error: Argument not Found')
    test_ed = request.args.get('test_ed', 'Error: Argument not Found')
    sv = request.args.get('sv', 'Error: Argument not Found')
    sma_window = request.args.get('sma_window', 'Error: Argument not Found')
    bollinger_band_sma = request.args.get('bollinger_band_sma', 'Error: Argument not Found')
    bollinger_band_stdev = request.args.get('bollinger_band_stdev', 'Error: Argument not Found')
    so_window = request.args.get('so_window', 'Error: Argument not Found')
    so_window_sma = request.args.get('so_window_sma', 'Error: Argument not Found')
    obv = request.args.get('obv', 'Error: Argument not Found')
    mom_window = request.args.get('mom_window', 'Error: Argument not Found')
    alpha = request.args.get('alpha', 'Error: Argument not Found')
    gamma = request.args.get('gamma', 'Error: Argument not Found')
    rar = request.args.get('rar', 'Error: Argument not Found')
    radr = request.args.get('radr', 'Error: Argument not Found')

    ## I checked documentation, and requests.args returns an Immutable Dict that implements all the regular Dict Methods
    ## Not sure how you want to pass these variables to run_pipeline, but you could essentially create class variables
    ## using the above arguments and runpipeline() that way.

    ## Regardless, all requested input variables have been passed
    ## successfully from front-end to your code

    return jsonify(request.args)

@app.route("/indicators_v2")
def indicators_v2():

    sma_window = int(request.args.get('sma_window', 'Error: Argument not Found'))
    bollinger_band_sma = int(request.args.get('bollinger_band_sma', 'Error: Argument not Found'))
    bollinger_band_stdev = int(request.args.get('bollinger_band_stdev', 'Error: Argument not Found'))
    so_window = int(request.args.get('so_window', 'Error: Argument not Found'))
    so_window_sma = int(request.args.get('so_window_sma', 'Error: Argument not Found'))
    obv = bool(request.args.get('obv', 'Error: Argument not Found'))
    mom_window = int(request.args.get('mom_window', 'Error: Argument not Found'))

    return run_pipeline_helper(sma_window, bollinger_band_sma, bollinger_band_stdev, so_window, so_window_sma, obv, mom_window)


'''
1) To Run the Flask App, simply run the file
2) On your Local Browser go to following home page: http://127.0.0.1:5000 
3) To view parameters being passed, go to following page:
http://127.0.0.1:5000/indicators?ticker=BTC&training_sd=None&training_ed=14&test_sd=3&test_ed=14&sv=14&sma_window=None&bollinger_band_sma=14&bollinger_band_stdev=3&so_window=14&so_window_sma=14&obv=27&mom_window=None&alpha=0.1&gamma=0.9&rar=0.99&radr=0.88

You should see a dictionary with all the indicator parameters, please ping me if you don't :)

Next Steps -> Take Parameters, pass it to runpipeline() -> Send me json object (Currently, I am returning JSON(Input))

'''
if __name__ == '__main__':
    with app.test_request_context():
        url = url_for('indicators', ticker = 'BTC', training_sd = 'None', training_ed = '14', test_sd = '3', test_ed = '14', sv='14', sma_window='None',bollinger_band_sma='14', bollinger_band_stdev='3', so_window='14', so_window_sma='14', obv='27', mom_window='None', alpha='0.1', gamma='0.9', rar='0.99', radr='0.88')
        url2 = url_for('indicators_v2', sma_window='14', bollinger_band_sma='20', bollinger_band_stdev='2', so_window='14', so_window_sma='3', obv='True', mom_window='14')
        print(url2)
    app.run(debug=True)
