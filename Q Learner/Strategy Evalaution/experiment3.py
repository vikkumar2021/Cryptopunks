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
  		  	   		   	 		  		  		    	 		 		   		 		  

def author(self):
    return "thabibe3"

# this method should use the existing policy and test it against new data
def df_to_order(df, symbol, sd=dt.datetime(2014, 9, 20), ed=dt.datetime(2020, 12, 31)):

    df = df.reset_index()
    df = df.rename(columns={'index' : 'Date'})
    df = df[df['Shares'] != 0]
    df['Order'] = 0
    df['Order'][df['Shares'] < 0] = 'SELL'
    df['Order'][df['Shares'] > 0] = 'BUY'
    df['Symbol'] = symbol
    df['Shares'] = abs(df['Shares'])
    df = df.reset_index(drop=True)
    
    if df['Order'].loc[len(df)-1] > 'BUY':
        lastorder = pd.DataFrame([(ed,1000,'SELL',symbol)], columns=df.columns)
        df = pd.concat([df,lastorder],axis=0)
    else:
        lastorder = pd.DataFrame([(ed,1000,'BUY',symbol)], columns=df.columns)
        df = pd.concat([df,lastorder],axis=0)
    df = df.reset_index(drop=True)
    return df

def main():
    
    #Training#
    pd.set_option('mode.chained_assignment', None)

    symbol = 'BTC'
    sd = dt.datetime(2018, 1, 1)
    ed = dt.datetime(2020, 12, 30)
    sv = 1000000

    SLlearner = StrategyLearner(alpha=0.05,
                 gamma=0.95,
                 rar=0.99,
                 radr=0.9)
    SLlearner.add_evidence(symbol, sd, ed)
    df1 = SLlearner.testPolicy(symbol, sd, ed)
    
    df1 = df_to_order(df=df1, symbol=symbol, sd=sd, ed=ed)
    
    dfgains1 = compute_portvals(df1, start_val=sv)

    order = [(1000, sd, 'BUY', symbol),
             (1000, ed, 'SELL', symbol)]
    
    dfbench = pd.DataFrame(order, columns=['Shares', 'Date', 'Order', 'Symbol'])
    benchmark = compute_portvals(dfbench, start_val=sv)

    dfgains1['Sum'] = ((dfgains1['Sum'] / dfgains1['Sum'].iloc[0]) - 1)
    benchmark['Sum'] = ((benchmark['Sum'] / benchmark['Sum'].iloc[0])- 1)

    fig, ax = plt.subplots(dpi=100)
    dfgains1.plot(color='g', label='Strategy Learner', ax=ax)
    benchmark.plot(color='b', label='Benchmark', ax=ax)
    plotline = True
    if plotline:
        for i in range(len(df1)):
            if df1['Order'][i] == 'BUY':
                ax.axvline(x=df1['Date'][i], color='g')
            else:
                ax.axvline(x=df1['Date'][i], color='r')
                
    plt.legend(['Strategy Learner', 'Benchmark'])
    plt.title('Portfolio Value Strategy Comparison ')
    plt.ylabel('Normalized Portfolio Values')
    plt.xlabel('Date')
    plt.savefig('experiment3.png')
    
    #Testing#
    
    symbol = 'BTC'
    sd = dt.datetime(2021, 1, 1)
    ed = dt.datetime(2022, 3, 30)
    sv = 1000000

    df2 = SLlearner.testPolicy(symbol, sd, ed)
    
    df2 = df_to_order(df=df2, symbol=symbol, sd=sd, ed=ed)
    dfgains2 = compute_portvals(df2, start_val=sv)

    order = [(1000, sd, 'BUY', symbol),
             (1000, ed, 'SELL', symbol)]
    
    dfbench = pd.DataFrame(order, columns=['Shares', 'Date', 'Order', 'Symbol'])
    benchmark = compute_portvals(dfbench, start_val=sv)
    
    dfgains2['Sum'] = ((dfgains2['Sum'] / dfgains2['Sum'].iloc[0]) - 1)
    benchmark['Sum'] = ((benchmark['Sum'] / benchmark['Sum'].iloc[0])- 1)
    
    print('Strategy')
    print(dfgains2.head)
    print()
    print('BTC')
    print(benchmark.head)
    
    
    fig2, ax2 = plt.subplots(dpi=100)
    
    dfgains2.plot(color='g', label='Strategy Learner', ax=ax2)
    
    benchmark.plot(color='b', label='Benchmark', ax=ax2)
    plotline = True
    if plotline:
        for i in range(len(df2)):
            if df2['Order'][i] == 'BUY':
                ax2.axvline(x=df2['Date'][i], color='g')
            else:
                ax2.axvline(x=df2['Date'][i], color='r')
    
    plt.legend(['Strategy Learner', 'Benchmark'])
    plt.title('Portfolio Value Strategy Comparison')
    plt.ylabel('Normalized Portfolio Values')
    plt.xlabel('Date')
    plt.savefig('experiment4.png')
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    main()
