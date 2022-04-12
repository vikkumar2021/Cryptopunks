""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		   	 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		   	 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		   	 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 		  		  		    	 		 		   		 		  
or edited.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		   	 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		   	 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Student Name: Tommy Habibe (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: thabibe3 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 902970734 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt
import numpy as np
import pandas as pd
from util import get_data, plot_data
from marketsimcode import compute_portvals, stats
import matplotlib.pyplot as plt
import math
from ManualLearner import ManualLearner
from StrategyLearner import StrategyLearner
  		  	   		   	 		  		  		    	 		 		   		 		  

def author(self):
    return "thabibe3"

# this method should use the existing policy and test it against new data
def df_to_order(df, symbol):

    df = df.reset_index()
    df = df.rename(columns={'index' : 'Date'})
    df = df[df['Shares'] != 0]
    df['Order'] = 0
    df['Order'][df['Shares'] < 0] = 'SELL'
    df['Order'][df['Shares'] > 0] = 'BUY'
    df['Symbol'] = symbol
    df['Shares'] = abs(df['Shares'])
    df = df.reset_index(drop=True)

    return df

def main():
    pd.set_option('mode.chained_assignment', None)

    symbol = 'BTC'
    sd = dt.datetime(2015, 1, 1)
    ed = dt.datetime(2020, 12, 31)
    c = 9.95
    i = 0.005
    sv = 1000000

    learner = ManualLearner(commission=c, impact=i)
    dfm = learner.testPolicy(symbol, sd, ed)
    df = df_to_order(dfm, symbol)
    dfgains = compute_portvals(df, start_val=sv, commission=c, impact=i)

    SLlearner = StrategyLearner(commission=c, impact=i)
    SLlearner.add_evidence(symbol, sd, ed)
    df1 = SLlearner.testPolicy(symbol, sd, ed)
    df1 = df_to_order(df=df1, symbol=symbol)
    dfgains1 = compute_portvals(df1, start_val=sv, commission=c, impact=i)

    order = [(1000, sd, 'BUY', symbol),
             (1000, ed, 'SELL', symbol)]
    dfbench = pd.DataFrame(order, columns=['Shares', 'Date', 'Order', 'Symbol'])
    benchmark = compute_portvals(dfbench, start_val=sv, commission=c, impact=i)

    dfgains = dfgains / dfgains.iloc[0]
    dfgains1 = dfgains1 / dfgains1.iloc[0]
    benchmark = benchmark / benchmark.iloc[0]

    fig, ax = plt.subplots(dpi=100)
    dfgains.plot(color='r', label='Manual Learner', ax=ax)
    dfgains1.plot(color='g', label='Strategy Learner', ax=ax)
    benchmark.plot(color='b', label='Benchmark', ax=ax)
    plt.legend(['Manual Learner', 'Strategy Learner', 'Benchmark'])
    plt.title('Portfolio Value Strategy Comparison ')
    plt.ylabel('Normalized Portfolio Values')
    plt.xlabel('Date')
    plt.savefig('experiment1.png')
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    main()
