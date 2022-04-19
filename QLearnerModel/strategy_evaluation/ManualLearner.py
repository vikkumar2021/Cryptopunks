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
import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .indicators import (MACD, bollinger_bands, momentum, price_sma_ratio,
                         stochastic_oscillator)
from .marketsimcode import compute_portvals, stats
from .util import get_data, plot_data


class ManualLearner(object):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		   	 		  		  		    	 		 		   		 		  
        If verbose = False your code should not generate ANY output.  		  	   		   	 		  		  		    	 		 		   		 		  
    :type verbose: bool  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The commission amount charged, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    """

    def author(self):
        return "thabibe3"

    # constructor  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		   	 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		   	 		  		  		    	 		 		   		 		  
        self.commission = commission

    # this method should use the existing policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(self, symbol="BTC", sd=dt.datetime(2014, 9, 20), ed=dt.datetime(2020, 12, 31), sv=1000000):

        spy = get_data([symbol], pd.date_range(sd, ed))
        spy.drop(columns=['SPY'], inplace=True)

        prices = spy.reset_index()
        # display(prices)

        bb = bollinger_bands(spy)
        moment = stochastic_oscillator(spy)
        sma = price_sma_ratio(spy)

        dfm = pd.concat([bb, moment, sma], axis=1)
        dfm = dfm.dropna()
        # display(dfm)

        dfmlist = dfm.values.tolist()

        dfm = dfm.reset_index()
        # display(dfm)
        # print(dfmlist)

        dates = dfm[['index']].reset_index(drop=True)
        # display(dates)

        trades = np.zeros(len(dfmlist))
        holdingslist = []
        buyind = []
        sellind = []
        holdings = 0

        for i in range(len(dfmlist)):

            buy = sum([x == 1 for x in dfmlist[i]])
            buyind.append(buy)

            sell = sum([x == 2 for x in dfmlist[i]])
            sellind.append(sell)

            if (holdings == 0):

                if (buy > 0) :
                    trades[i] = 1000
                    holdings = holdings + 1000
                elif (sell > 0):
                    trades[i] = -1000
                    holdings = holdings - 1000

            else:

                if (buy > 0) & (holdings < 0):
                    trades[i] = 2000
                    holdings = holdings + 2000
                elif (sell > 0) & (holdings > 0):
                    trades[i] = -2000
                    holdings = holdings - 2000

            if (holdings < -1000) | (holdings > 1000):
                print('HOLDINGS EROOOOOOR')

            holdingslist.append(holdings)

        # print(holdingslist)

        inddf = pd.DataFrame(list(zip(buyind, sellind, holdingslist)), columns=['buyind', 'sellind', 'holdings'])
        # display(inddf)

        pd.set_option('mode.chained_assignment', None)

        orders = trades.tolist()
        df = pd.DataFrame(orders, columns=['Shares'])
        df1 = df.copy()
        df1 = df1.join(prices)
        df1.drop(columns=symbol, inplace=True)
        df1 = df1.set_index('index')

        df['Date'] = dates
        # df['Price'] = p
        df = df[df['Shares'] != 0]
        df['Order'] = 0
        df['Order'][df['Shares'] < 0] = 'SELL'
        df['Order'][df['Shares'] > 0] = 'BUY'
        df['Symbol'] = symbol
        df['Shares'] = abs(df['Shares'])
        df = df.reset_index(drop=True)

        # display(df)

        gains = compute_portvals(df, start_val=sv, commission=self.commission, impact=self.impact)
        order = [(1000, prices['index'].loc[0], 'BUY', symbol), (0, prices['index'].loc[len(prices) - 1], 'SELL', symbol)]
        dfbench = pd.DataFrame(order, columns=['Shares', 'Date', 'Order', 'Symbol'])
        benchmark = compute_portvals(dfbench, start_val=sv, commission=self.commission, impact=self.impact)

        benchmark = benchmark.rename(columns={'Sum': 'Benchmark'})
        gains = gains.rename(columns={'Sum': 'Manual Strategy'})

        benchmarkstats = stats(benchmark)
        gainsstats = stats(gains)

        textfile = open("p6_results.txt", "w")
        statname = ['cum_ret', 'avg_daily_ret', 'std_daily_ret', 'sharpe_ratio']
        textfile.write("Theoretically Optimal Strategy \n")
        for s, g in zip(statname, gainsstats):
            textfile.write(s + ': ' + str(g) + "\n")
        textfile.write('Portfolio Value: ' + str(gains.values[len(gains) - 1][0]) + "\n")

        textfile.write("\n")
        textfile.write("Benchmark \n")
        for s, g in zip(statname, benchmarkstats):
            textfile.write(s + ': ' + str(g) + "\n")
        textfile.write('Portfolio Value: ' + str(benchmark.values[len(gains) - 1][0]) + "\n")

        textfile.close()

        gains = gains / gains.iloc[0]
        benchmark = benchmark / benchmark.iloc[0]

        fig, ax = plt.subplots(dpi=100)
        gains.plot(color='r', ax=ax)
        benchmark.plot(color='g', ax=ax)
        plt.title('Manual Learner vs Benchmark Portfolio Returns')
        plt.ylabel('Normalized Portfolio Values')
        plt.xlabel('Date')
        plt.savefig('manuallearner_' + symbol + '.png')

        return df1

def main():
    pd.set_option('mode.chained_assignment', None)
    learner = ManualLearner(commission=9.95, impact=0.005)
    df = learner.testPolicy()
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":
    main()

