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
import StrategyLearner as sl
  		  	   		   	 		  		  		    	 		 		   		 		  

def author(self):
    return "thabibe3"


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
    sd = dt.datetime(2014, 9, 20)
    ed = dt.datetime(2020, 12, 31)
    c = 0
    sv = 100000
    plt.figure(dpi=100)

    n = np.linspace(0, 0.01, 10)

    spy = get_data([symbol], pd.date_range(sd, ed))
    spy.drop(columns=['SPY'], inplace=True)

    slist = []

    for i in range(len(n)):
        SLlearner = sl.StrategyLearner(commission=c, impact=n[i])
        SLlearner.add_evidence(symbol, sd, ed)
        df1 = SLlearner.testPolicy(symbol, sd, ed)
        df1 = df_to_order(df=df1, symbol=symbol)
        dfgains1 = compute_portvals(df1, start_val=sv, commission=c, impact=n[i])

        total_adjusted_cum_return, total_adjusted_avg_daily_ret, total_adjusted_std_daily_ret, sharp = stats(dfgains1)

        slist.append([total_adjusted_cum_return, total_adjusted_avg_daily_ret, total_adjusted_std_daily_ret, sharp])

        dfgains1 = dfgains1 / dfgains1.iloc[0]
        dfgains1 = dfgains1.rename(columns={'Sum': str(n[i])})
        spy = spy.join(dfgains1)

    spy = spy.drop(columns=symbol)
    spy.plot()
    plt.legend([str(x) for x in np.linspace(0, 0.05, 10)],prop={'size':6})
    plt.title('Effect of Market Impact Value on Strategy Learner')
    plt.ylabel('Normalized Portfolio Values')
    plt.xlabel('Date')
    plt.savefig('experiment2.png')

    with open('experiment2.txt', 'w') as f:
        lista = ['cum sum', 'daily ret', 'daily stdev', 'sharpe']

        for r in lista:
            f.write(r + ',')
        f.write('\n')

        for s in slist:
            for i in s:
                f.write(str(i) + ',')
            f.write('\n')

    f.close()

if __name__ == "__main__":
    main()