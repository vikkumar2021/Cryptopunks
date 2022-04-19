import sys
import math

sys.path.insert(0,r"C:\Users\tthab\Documents\GitHub\Cryptopunks\cryptopunks_data_pipeline")
sys.path.insert(0,r"C:\Users\tthab\Documents\GitHub\Cryptopunks")

import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data
from marketsimcode import compute_portvals, stats
import matplotlib.pyplot as plt
import math
from ManualLearner import ManualLearner
from StrategyLearner import StrategyLearner
import json
from cryptopunks_data_pipeline import *
from cryptopunks_data_pipeline.data_preparation_pipeline import run_pipeline 
import os
import sys
from cryptopunks_data_pipeline.data_preparation_pipeline import create_spark_session
from dataframe_binning import categorize_pipeline as bdfcp
from datetime import datetime
  		  	   		   	 		  		  		    	 		 		   		 		  

def author(self):
    return "thabibe3"

# this method should use the existing policy and test it against new data
def df_to_order(df, symbol, sd=dt.datetime(2014, 9, 20), ed=dt.datetime(2020, 12, 31)):

    df = df.reset_index()
    df = df.rename(columns={'index' : 'TradeDate'})
    df = df[df['Shares'] != 0]
    df['Order'] = 0
    df['Order'][df['Shares'] < 0] = 'SELL'
    df['Order'][df['Shares'] > 0] = 'BUY'
    df['Symbol'] = symbol
    df['Shares'] = abs(df['Shares'])
    df = df.reset_index(drop=True)
    
# =============================================================================
#     if df['Order'].loc[len(df)-1] == 'BUY':
#         lastorder = pd.DataFrame([(ed,1000,'SELL',symbol)], columns=df.columns)
#         df = pd.concat([df,lastorder],axis=0)
#     else:
#         lastorder = pd.DataFrame([(ed,1000,'BUY',symbol)], columns=df.columns)
#         df = pd.concat([df,lastorder],axis=0)
#     df = df.reset_index(drop=True)
# =============================================================================
    return df

def main():
    
    with open("config_file.json") as f:

        config = json.load(f)
    
    symbol = config.get("ticker")
    
    training_sd = datetime.strptime(config.get("training_sd"),"%Y-%m-%d")
    training_ed = datetime.strptime(config.get("training_ed"),"%Y-%m-%d")
    test_sd = datetime.strptime(config.get("test_sd"),"%Y-%m-%d")
    test_ed = datetime.strptime(config.get("test_ed"),"%Y-%m-%d")

    sv = config.get("sv")
    
    sma_window1 = config.get("sma_window")
    bollinger_band_sma = config.get("bollinger_band_sma")
    bollinger_band_stdev = config.get("bollinger_band_stdev")
    so_window = config.get("so_window")
    so_window_sma = config.get("so_window_sma")
    obv = config.get("obv")
    mom_window = config.get("mom_window")
    macd_window = config.get("macd")
    include_sentiment = config.get("include_sentiment")
    
    alpha = config.get("alpha")
    gamma = config.get("gamma")
    rar = config.get("rar")
    radr = config.get("radr") 
    
    spark = create_spark_session()
    
    dataframebtc = run_pipeline(spark, include_sentiment=include_sentiment,
                    sma_window = sma_window1,
                    bollinger_window = bollinger_band_sma,
                    bollinger_stdvs =bollinger_band_stdev,
                    so_window = so_window,
                    so_window_sma = so_window_sma,
                    obv = obv,
                    macd = macd_window,
                    mom_window = mom_window)
    
    #dataframebtc.to_csv('pipeline.csv')
    
    binned_df, combos = bdfcp(dataframebtc)
    
    binned_df = binned_df.dropna().reset_index(drop=True)
    #print(binned_df.head)
    #print(combos)
    
    #Training#
    pd.set_option('mode.chained_assignment', None)

    symbol = symbol
    sd = training_sd
    ed = training_ed
    sv = sv

    SLlearner = StrategyLearner(num_states=combos,
                                alpha=alpha,
                                gamma=gamma,
                                rar=rar,
                                radr=radr)
    
    SLlearner.add_evidence(binned_df, sd, ed, sv)
    df1 = SLlearner.testPolicy(binned_df, sd, ed, sv)
    df1 = df_to_order(df=df1, symbol=symbol, sd=sd, ed=ed)
    
    dfgains1 = compute_portvals(df1, start_val=sv)
    
    #print(sv/dataframebtc['Adj_Close'][0])
    order = [(sd, math.floor(sv/dataframebtc['Adj_Close'][dataframebtc['TradeDate']==sd]), 'BUY', symbol),
             (ed, math.floor(sv/dataframebtc['Adj_Close'][dataframebtc['TradeDate']==sd]), 'SELL', symbol)]
    
    dfbench = pd.DataFrame(order, columns=['TradeDate', 'Shares', 'Order', 'Symbol'])
    benchmark = compute_portvals(dfbench, start_val=sv)
    #print(benchmark.head)

    dfgains1['Sum'] = ((dfgains1['Sum']  / dfgains1['Sum'].iloc[0]))
    benchmark['Sum'] = ((benchmark['Sum'] / benchmark['Sum'].iloc[0]))
    
    #print(dfgains1.head)
    #print(benchmark.head)

# =============================================================================
#     fig, ax = plt.subplots(dpi=100)
#     dfgains1.plot(color='g', label='Strategy Learner', ax=ax)
#     benchmark.plot(color='b', label='Benchmark', ax=ax)
#     plotline = True
#     if plotline:
#         for i in range(len(df1)):
#             if df1['Order'][i] == 'BUY':
#                 ax.axvline(x=df1['TradeDate'][i], color='g',alpha=0.5)
#             else:
#                 ax.axvline(x=df1['TradeDate'][i], color='r',alpha=0.5)
#     
#     ax.set_xlim([sd,ed])
#     plt.legend(['Strategy Learner', 'Benchmark'])
#     plt.title('Portfolio Value Strategy Comparison ')
#     plt.ylabel('Normalized Portfolio Values')
#     plt.xlabel('TradeDate')
#     plt.savefig('experiment3.png')
# =============================================================================
    
    #Testing#
    
    symbol = 'BTC'
    sd2 = test_sd
    ed2 = test_ed
    sv2 = sv

    df2 = SLlearner.testPolicy(binned_df, sd2, ed2, sv)
    
    df2 = df_to_order(df=df2, symbol=symbol, sd=sd2, ed=ed2)
    

    dfgains2 = compute_portvals(df2, start_val=sv)

    order2 = [(sd2, math.floor(sv/dataframebtc['Adj_Close'][dataframebtc['TradeDate']==sd2]), 'BUY', symbol),
             (ed2, math.floor(sv/dataframebtc['Adj_Close'][dataframebtc['TradeDate']==sd2]), 'SELL', symbol)]
    
    dfbench2 = pd.DataFrame(order2, columns=['TradeDate', 'Shares', 'Order', 'Symbol'])
    benchmark2 = compute_portvals(dfbench2, start_val=sv)
    
    dfgains2['Sum'] = ((dfgains2['Sum'] / dfgains2['Sum'].iloc[0]))
    benchmark2['Sum'] = ((benchmark2['Sum'] / benchmark2['Sum'].iloc[0]))

    
    #print(dfgains2.head)
    #print(benchmark2.head)
    
    
    #print('Strategy')
    #print(dfgains2.head)
    #print()
    #print('BTC')
    #print(benchmark.head)
    
    
# =============================================================================
#     fig2, ax2 = plt.subplots(dpi=100)
#     
#     dfgains2.plot(color='g', label='Strategy Learner', ax=ax2)
#     
#     benchmark2.plot(color='b', label='Benchmark', ax=ax2)
#     plotline = True
#     if plotline:
#         for i in range(len(df2)):
#             if df2['Order'][i] == 'BUY':
#                 ax2.axvline(x=df2['TradeDate'][i], color='g',alpha=0.5)
#             else:
#                 ax2.axvline(x=df2['TradeDate'][i], color='r',alpha=0.5)
#     ax2.set_xlim([sd2,ed2])
#     plt.legend(['Strategy Learner', 'Benchmark'])
#     plt.title('Portfolio Value Strategy Comparison')
#     plt.ylabel('Normalized Portfolio Values')
#     plt.xlabel('TradeDate')
#     plt.savefig('experiment4.png')
#     
#     df2.to_csv('orders.csv')
#     dfgains2.to_csv('gains.csv')
# =============================================================================
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    main()
