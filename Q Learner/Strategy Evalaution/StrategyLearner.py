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
import random
import numpy as np
import pandas as pd
from util import get_data, plot_data
from marketsimcode import compute_portvals, stats
import matplotlib.pyplot as plt
import math
from indicators import price_sma_ratio, bollinger_bands, MACD, momentum, stochastic_oscillator
import QLearner as ql
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class StrategyLearner(object):
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
    def __init__(self,
                 impact=0.0,
                 commission=0.0,
                 num_states=27,
                 num_actions=3,
                 alpha=0.1,
                 gamma=0.9,
                 rar=0.99,
                 radr=0.8,		  	   		   	 		  		  		    	 		 		   		 		  
                 dyna=0,  		  	   		   	 		  		  		    	 		 		   		 		  
                 verbose=False):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Constructor method  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        self.verbose = verbose  		  	   		   	 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		   	 		  		  		    	 		 		   		 		  
        self.commission = commission
        self.learner = ql.QLearner(
        num_states=27,
        num_actions=3,
        alpha=0.1,
        gamma=0.9,
        rar=0.99,
        radr=0.8,
        dyna=0,
        verbose=False)
        
        self.cols = [('bollinger_band_percentage',3),
            ('stochastic_oscillator_sma',3),
            ('rsi',3),
            ("price_to_SMA_ratio", 3),
            ("momentum", 2),
            ('avg_compound_sentiment', 3),
            ('macd', 2)]
        

    def state_calc(self,stringi):

        state = (int(stringi[0]) * 6 + int(stringi[1]) * 2 + int(stringi[2]))-1

        return state

    def list_to_string(self,lista):
        return str(lista[0]) + str(lista[1]) + str(lista[2])

    def add_evidence(self, data, sd, ed, sv=1000000):
        
        symbol = 'Adj_Close'
        
        #data = data[(data['TradeDate']>=sd) & (data['TradeDate']<=ed)]
        print(len(data))

        dfmlist = data.iloc[:,2:].values.tolist()
        dates = data.iloc[:,:1]
        prices = data.iloc[:,:2]
        
        buyind = []
        sellind = []


        totalrewardold = -9999
        totalreward = 0
        count1 = 0
        count = 0
        while (count < 5) & (count1 < 1000):

            tradesdf = np.zeros(len(dfmlist))
            impactdf = np.zeros(len(dfmlist))
            commissiondf = np.zeros(len(dfmlist))
            costdf = np.zeros(len(dfmlist))
            cashdf = np.zeros(len(dfmlist))
            cashdf[0] = sv
            val = np.zeros(len(dfmlist))
            holdingsdf = np.zeros(len(dfmlist))
            holdvaldf = np.zeros(len(dfmlist))
            rewarddf = np.zeros(len(dfmlist))

            holdings = 0
            cash = sv

            totalrewardold = totalreward
            totalreward = 0

            for i in range(len(dfmlist)):

                if not any(np.isnan(dfmlist[i])):

                    lista = [int(x) for x in dfmlist[i]]

                    # print(dfmlist[i])
                    # print(state_calc(list_to_string(lista)))

                    if holdings == 0:

                        action = self.learner.querysetstate(self.state_calc(self.list_to_string(lista)))

                        # print(action)

                        if (action == 0) & (holdings == 0):

                            tradesdf[i] = 1000
                            holdings = 1000
                            holdingsdf[i] = holdings
                            impactdf[i] = abs(tradesdf[i]) * self.impact
                            commissiondf[i] = self.commission


                        elif (action == 1) & (holdings == 0):

                            tradesdf[i] = -1000
                            holdings = -1000
                            holdingsdf[i] = holdings
                            impactdf[i] = abs(tradesdf[i]) * self.impact
                            commissiondf[i] = self.commission

                        else:

                            tradesdf[i] = 0
                            holdingsdf[i] = holdings

                    else:

                        action = self.learner.query(self.state_calc(self.list_to_string(lista)), reward)
                        # print(action)

                        if (action == 0) & (holdings < 0):

                            tradesdf[i] = 2000
                            holdings = holdings + 2000
                            holdingsdf[i] = holdings
                            impactdf[i] = abs(tradesdf[i]) * self.impact
                            commissiondf[i] = self.commission


                        elif (action == 1) & (holdings > 0):

                            tradesdf[i] = -2000
                            holdings = holdings - 2000
                            holdingsdf[i] = holdings
                            impactdf[i] = abs(tradesdf[i]) * self.impact
                            commissiondf[i] = self.commission

                        else:

                            tradesdf[i] = 0
                            holdingsdf[i] = holdings

                if i == 0:

                    costdf[i] = -tradesdf[i] * prices[symbol][i] + prices[symbol][i] * impactdf[i] + commissiondf[i]
                    cashdf[i] = sv + costdf[i]
                    holdvaldf[i] = holdingsdf[i] * prices[symbol][i]
                    val[i] = holdingsdf[i] * prices[symbol][i] + cashdf[i]
                    reward = val[i] - sv
                    rewarddf[i] = reward / sv

                else:

                    costdf[i] = -tradesdf[i] * prices[symbol][i] + prices[symbol][i] * impactdf[i] + commissiondf[i]
                    cashdf[i] = cashdf[i - 1] + costdf[i]
                    holdvaldf[i] = holdingsdf[i] * prices[symbol][i]
                    val[i] = holdingsdf[i] * prices[symbol][i] + cashdf[i]
                    reward = val[i] - val[i - 1]
                    rewarddf[i] = reward / val[i - 1]

                totalreward = totalreward + reward

            #print(totalreward)
            count1 = count1 + 1

            if (abs(totalreward - totalrewardold) < 4000):
                count = count + 1
            else:
                count = 0

        summary = pd.DataFrame(
            zip(prices[symbol].tolist(), holdingsdf.tolist(), tradesdf.tolist(), costdf.tolist(), cashdf.tolist(),
                val.tolist(), rewarddf.tolist()))


    # this method should use the existing policy and test it against new data
    def testPolicy(self, data, sd, ed, sv=1000000):
        #data = data[(data['TradeDate']>=sd) & (data['TradeDate']<=ed)]
        print(len(data))
        
        symbol = 'Adj_Close'

        dfmlist = data.iloc[:,2:].values.tolist()
        dates = data.iloc[:,:1]
        prices = data.iloc[:,:2]


        tradesdf = np.zeros(len(dfmlist))
        impactdf = np.zeros(len(dfmlist))
        commissiondf = np.zeros(len(dfmlist))
        costdf = np.zeros(len(dfmlist))
        cashdf = np.zeros(len(dfmlist))
        val = np.zeros(len(dfmlist))
        holdingsdf = np.zeros(len(dfmlist))

        holdings = 0
        cash = sv

        totalreward = 0

        for i in range(len(dfmlist)):

            if not any(np.isnan(dfmlist[i])):

                lista = [int(x) for x in dfmlist[i]]

                # print(dfmlist[i])
                # print(state_calc(list_to_string(lista)))

                if holdings == 0:

                    action = self.learner.querysetstate(self.state_calc(self.list_to_string(lista)))

                    # print(action)

                    if (action == 0) & (holdings == 0):

                        tradesdf[i] = 1000
                        holdings = 1000
                        holdingsdf[i] = holdings
                        impactdf[i] = abs(tradesdf[i]) * self.impact
                        commissiondf[i] = self.commission


                    elif (action == 1) & (holdings == 0):

                        tradesdf[i] = -1000
                        holdings = -1000
                        holdingsdf[i] = holdings
                        impactdf[i] = abs(tradesdf[i]) * self.impact
                        commissiondf[i] = self.commission

                    else:

                        tradesdf[i] = 0
                        holdingsdf[i] = holdings

                else:

                    action = self.learner.querysetstate(self.state_calc(self.list_to_string(lista)))
                    # print(action)

                    if (action == 0) & (holdings < 0):

                        tradesdf[i] = 2000
                        holdings = holdings + 2000
                        holdingsdf[i] = holdings
                        impactdf[i] = abs(tradesdf[i]) * self.impact
                        commissiondf[i] = self.commission


                    elif (action == 1) & (holdings > 0):

                        tradesdf[i] = -2000
                        holdings = holdings - 2000
                        holdingsdf[i] = holdings
                        impactdf[i] = abs(tradesdf[i]) * self.impact
                        commissiondf[i] = self.commission

                    else:

                        tradesdf[i] = 0
                        holdingsdf[i] = holdings

        pd.set_option('mode.chained_assignment', None)

        orders = tradesdf.tolist()
        df = pd.DataFrame(orders, columns=['Shares'])
        df1 = df.copy()
        df1 = df1.join(prices)
        df1.drop(columns=symbol, inplace=True)
        df1 = df1.set_index('TradeDate')

# =============================================================================
#         #print(df1)
#         df['Date'] = dates
#         # df['Price'] = p
#         df = df[df['Shares'] != 0]
#         df['Order'] = 0
#         df['Order'][df['Shares'] < 0] = 'SELL'
#         df['Order'][df['Shares'] > 0] = 'BUY'
#         df['Symbol'] = symbol
#         df['Shares'] = abs(df['Shares'])
#         df = df.reset_index(drop=True)
# 
#         gains = compute_portvals(df, start_val=sv, commission=self.commission, impact=self.impact)
#         #print(gains.iloc[-1])
# 
#         order = [(1000, prices['index'].loc[0], 'BUY', symbol),
#                  (1000, prices['index'].loc[len(prices) - 1], 'SELL', symbol)]
# 
#         dfbench = pd.DataFrame(order, columns=['Shares', 'Date', 'Order', 'Symbol'])
#         benchmark = compute_portvals(dfbench, start_val=sv, commission=self.commission, impact=self.impact)
# 
#         benchmark = benchmark.rename(columns={'Sum': 'Benchmark'})
#         gains = gains.rename(columns={'Sum': 'Strategy Learner'})
# 
#         gains = gains / gains.iloc[0]
#         benchmark = benchmark / benchmark.iloc[0]
#         
#         print(benchmark.head)
# 
#         #fig, ax = plt.subplots(dpi=100)
#         #gains.plot(color='r', ax=ax)
#         #benchmark.plot(color='g', ax=ax)
#         #plt.title('Strategy Learner vs Benchmark Portfolio Returns')
#         #plt.ylabel('Normalized Portfolio Values')
#         #plt.xlabel('Date')
#         #plt.savefig('strategylearner_' + symbol + '.png')
# =============================================================================

        return df1

def main():
    pd.set_option('mode.chained_assignment', None)

    symbol = 'BTC'
    sd = dt.datetime(2018, 1, 1)
    ed = dt.datetime(2020, 12, 31)

    SLlearner = StrategyLearner(commission=0, impact=0)
    SLlearner.add_evidence(symbol, sd, ed)
    
    sd1 = dt.datetime(2021, 1, 1)
    ed1 = dt.datetime(2022, 3, 31)
    
    #sd1 = dt.datetime(2021, 1, 1)
    #ed1 = dt.datetime(2022, 3, 1)

    SLlearner.testPolicy(symbol, sd1, ed1)

if __name__ == "__main__":
    main()