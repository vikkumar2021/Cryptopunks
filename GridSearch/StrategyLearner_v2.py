# Minh Trang NGUYEN
# mnguyen306

import datetime as dt
import random
import math

import numpy as np
import pandas as pd
import scipy.optimize as spo
from .marketsimcode import marketsim_df
from .util import get_data


def get_sharpe_ratio(threshold, *params):
    indicator_1, indicator_2, indicator_3, normed, symbol_str, impact, dataframebtc, num_shares = params
    #sma, bbp, rsi, normed, symbol_str, impact, dataframebtc = params
    Date = []
    Symbol = []
    Order = []
    Shares = []
    SELL = []
    BUY = []
    orders = []
    syms = [symbol_str]
    holdings = {sym: 0 for sym in syms}



    for day in range(1, normed.shape[0]):
            if (
                (indicator_1[day] < threshold[0])
                and (indicator_2[day] < threshold[1])
                and (indicator_3[day] < threshold[1])
                and (-num_shares <= holdings[syms[0]] < num_shares)
            ):
                if holdings[syms[0]] < num_shares:  # stock oversold but index is not oversold
                    # print ('1111 ')
                    if holdings[syms[0]] == 0:
                        holdings[syms[0]] = holdings[syms[0]] + num_shares
                        Shares.append(num_shares)
                    else:  # hold = -1000
                        holdings[syms[0]] = holdings[syms[0]] + num_shares*2
                        Shares.append(num_shares*2)

                    orders.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("BUY")
            elif (
                (indicator_1[day] > threshold[2])
                and (indicator_2[day] > threshold[3])
                and (indicator_3[day] > threshold[3])
                and (-num_shares <= holdings[syms[0]] <= num_shares)
            ):  # stock overbought but index is not overbought
                if holdings[syms[0]] > 0:
                    # print ('2222 ')
                    if holdings[syms[0]] == 0:
                        holdings[syms[0]] = holdings[syms[0]] - num_shares
                        Shares.append(num_shares)
                    else:
                        holdings[syms[0]] = holdings[syms[0]] - num_shares*2
                        Shares.append(num_shares*2)

                    orders.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("SELL")
            elif (
                (indicator_1[day] >= (threshold[2]))
                and (indicator_1[day-1] < (threshold[2]))
                and (-num_shares < holdings[syms[0]] <= num_shares)
                and (-num_shares <= holdings[syms[0]] <= num_shares)
            ):  # crossed SMA upwards and hold long
                # print ('3333 ')
                if holdings[syms[0]] == 0:
                    holdings[syms[0]] = holdings[syms[0]] - num_shares
                    Shares.append(num_shares)

                else:
                    holdings[syms[0]] = holdings[syms[0]] - num_shares*2
                    Shares.append(num_shares*2)

                orders.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("SELL")
            elif (
                (indicator_1[day] <= (threshold[0]))
                and (indicator_1[day-1] > (threshold[0]))
                and (-num_shares <= holdings[syms[0]] < num_shares)
            ):  # crossed SMA downwards and hold short
                # print '4444 '
                if holdings[syms[0]] == 0:

                    holdings[syms[0]] = holdings[syms[0]] + num_shares
                    Shares.append(num_shares)
                else:
                    holdings[syms[0]] = holdings[syms[0]] + num_shares*2
                    Shares.append(num_shares*2)

                orders.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("BUY")

    #    print "NUM ORDERS => ", len(Order)
    if len(Order) == 0:
        return num_shares

    df = pd.DataFrame({"Symbol": Symbol}, index=Date)
    df["Order"] = Order
    df["Shares"] = Shares

    order = df


    syms = order.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end

    sd = normed.index[0]
    ed = normed.index[-1]
    dates = pd.date_range(sd, ed)

    commission = 0

    df_prices_all = dataframebtc
    df_prices = df_prices_all[["Adj_Close"]]
    df_prices = df_prices.rename(columns={"Adj_Close": "BTC"})
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)
    df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
    df_trade = df_trade.fillna(0)
    # print ('order = ', order)
    # print ('df_price = ', df_prices)
    # print ('df_trade = ', df_trade)
    for i, row in order.iterrows():  # go through each order
        # print ('i, row = ', i, row)
        # print ('df_trade.loc[i] = ', df_trade.loc[i])
        if row.Order == "BUY":
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] + row.Shares
            df_trade.loc[i]["CASH"] =  math.floor((row.Shares * df_prices.loc[i][row.Symbol]) * (-1))
            # df_trade.loc[i,row.Symbol] += row.Shares
            # df_trade.loc[i, 'CASH'] -= (row.Shares * ((1+impact)*df_prices.loc[i,row.Symbol])) - (commission)
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]["CASH"] = math.floor((row.Shares * df_prices.loc[i][row.Symbol]) * 1)

            # df_trade.loc[i,row.Symbol] -= row.Shares
            # df_trade.loc[i,'CASH'] +=(row.Shares * ((1-impact)*df_prices.loc[i,row.Symbol])) - (commission)
    df_holding = pd.DataFrame(index=df_prices.index, columns=cols)
    df_holding = df_holding.fillna(0)
    df_holding = df_trade.cumsum()
    start_val = 500000
    df_holding["CASH"] = df_holding["CASH"] + start_val
    # print df_holding
    #    print 'holding < -1000', (df_holding[symbol_str]<-1000).any()
    #    print 'holding > 1000', (df_holding[symbol_str]>1000).any()
    df_value = pd.DataFrame(index=df_prices.index, columns=cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            # df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]
            df_value.loc[i, sym] = row[sym] * df_prices.loc[i, sym]
    df_value["CASH"] = df_holding["CASH"]
    # print df_value
    portvals = df_value.sum(axis=1)

    cr = (portvals[-1] / portvals[0]) - 1
    # print("TH , last day portval = ", threshold, portvals[-1])
    # print("ORDERS = ", Order)
    return -portvals[-1]



class StrategyLearner(object):
    def __init__(self, verbose=False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.threshold = []

        self.sma = []
        self.bbp = []
        self.rsi = []

        self.num_order = 2
        self.cr = 0

    def author(self):
        return "mnguyen306"

    def addEvidence(
        self,
        input_df,
        symbol="IBM",
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 1, 1),
        sv=10000,
        num_shares=10
    ):

        symbol_str = symbol
        symbol = [symbol]
        dates = pd.date_range(sd, ed)
        # prices_all = get_data(symbol, dates, addSPY=False)
        prices_all = input_df
        prices = prices_all[["Adj_Close"]]
        prices = prices.rename(columns={"Adj_Close": "BTC"})
        prices.fillna(method="ffill", inplace=True)
        prices.fillna(method="bfill", inplace=True)
        normed = prices / prices.values[0, :]
        pos_vals = normed * sv
        port_val = pos_vals.sum(axis=1)
        prices_OURS_norm = port_val / port_val.values[0]
        daily_returns = (port_val / port_val.shift(1)) - 1
        daily_returns = daily_returns[1:]

        print(
            "********************* Add Evidence   ************************")

        indicator_1 = input_df['price_to_SMA_ratio']
        indicator_2 = input_df['momentum']
        indicator_3 = input_df['rolling_avg']


        initial_threshold = [0.95, 0.3, 1.05, 1]
        params = (indicator_1, indicator_2, indicator_3, normed, symbol_str, self.impact, input_df, num_shares)

        rranges_old = [
            slice(0.6, 1.01, 0.4),  #  SMA  RATIO
            slice(-0.2, 1.21, 0.4),  # BUY
            slice(1.0, 1.61, 0.4),  # SELL SMA
            slice(-0.2, 1.21, 0.4),  #  SELL BBP-RSI
        ] 
        min_1 = indicator_1.min()
        max_1 = indicator_1.max()
        mid_1 = round(((max_1 + min_1)/2) , 3)
        step_1 = round(((max_1 - min_1)/ 3), 3)/2

        min_2 = indicator_2.min()
        max_2 = indicator_2.max()
        mid_2 = round(((max_2 + min_2)/2) , 3)
        step_2 = round(((max_2 - min_2)/3 ), 3)/2

        min_3 = indicator_3.min()
        max_3 = indicator_3.max()
        mid_3 = round(((max_3 + min_3)/2) , 3)
        step_3 = round(((max_3 - min_3)/ 3), 3)/2

        print ('\nRRANGES')
        print ((min_1, mid_1, step_1))
        print ((min_2, mid_2, step_2))
        print ((mid_1, max_1, step_1))
        print ((mid_2, max_2, step_2))


        rranges = [
         slice(-0.31743839421422201, 0.162, 0.160),
         slice(-0.3637347457782, 0.431, 0.265),
         slice(0.162, 0.64165430406962668, 0.160),
         slice(0.431, 1.2266714932757, 0.265) ]
         

        threshold_brute = spo.brute(
            get_sharpe_ratio, rranges, args=params, full_output=True, finish=None
        )

        # self.threshold  = initial_threshold
        self.threshold = threshold_brute[0]
        print("========  self.threshold  ==========  ", self.threshold)
        # ========  self.threshold  ==========   [-0.22234573 -0.43464864  0.32065427 -0.43464864]

    def testPolicy(
        self,
        input_df,
        symbol="JPM",
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=100000,
        num_shares=10
    ):

        risk_free_rate = 0.0
        sample_freq = 252
        lookback = 10
        symbol_str = symbol
        symbol = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = input_df  # get_data(symbol, dates, addSPY=False)
        prices = prices_all[["Adj_Close"]]
        prices = prices.rename(columns={"Adj_Close": "BTC"})
        prices.fillna(method="ffill", inplace=True)
        prices.fillna(method="bfill", inplace=True)
        normed = prices / prices.values[0, :]
        pos_vals = normed * sv
        port_val = pos_vals.sum(axis=1)
        prices_OURS_norm = port_val / port_val.values[0]
        daily_returns = (port_val / port_val.shift(1)) - 1
        daily_returns = daily_returns[1:]

        print("********************* Test Policy ************************")


        indicator_1 = input_df['price_to_SMA_ratio']
        indicator_2 = input_df['momentum']
        indicator_3 = input_df['rolling_avg']

        Date = []
        Symbol = []
        Order = []
        Shares = []
        Date_all = []
        Symbol_all = []
        Order_all = []
        Shares_all = []
        SELL = []
        BUY = []
        orders = []
        orders_all=[]
        holdings = {sym: 0 for sym in symbol}
        syms = [symbol_str]

        for day in range(1, normed.shape[0]):
                if (
                    (indicator_1[day] < self.threshold[0])
                    and (indicator_2[day] < self.threshold[1])
                    and (indicator_3[day] < self.threshold[1])
                    and (-num_shares <= holdings[syms[0]] < num_shares)
                ):
                    if holdings[syms[0]] < 10:  # stock oversold but index is not oversold
                        # print ('1111 ')
                        if holdings[syms[0]] == 0:
                            holdings[syms[0]] = holdings[syms[0]] + num_shares
                            Shares.append(num_shares)
                            Shares_all.append(num_shares)
                        else:  # hold = -1000
                            holdings[syms[0]] = holdings[syms[0]] + num_shares*2
                            Shares.append(num_shares*2)
                            Shares_all.append(num_shares*2)

                        orders.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                        Date.append(normed.index[day])
                        Symbol.append(symbol_str)
                        Order.append("BUY")

                        orders_all.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                        Date_all.append(normed.index[day])
                        Symbol_all.append(symbol_str)
                        Order_all.append("BUY")
                elif (
                    (indicator_1[day] > self.threshold[2])
                    and (indicator_2[day] > self.threshold[3])
                    and (indicator_3[day] > self.threshold[3])
                    and (-num_shares <= holdings[syms[0]] <= num_shares)
                ):  # stock overbought but index is not overbought
                    if holdings[syms[0]] > 0:
                        # print ('2222 ')
                        if holdings[syms[0]] == 0:
                            holdings[syms[0]] = holdings[syms[0]] - num_shares
                            Shares.append(num_shares)
                            Shares_all.append(-num_shares)
                        else:
                            holdings[syms[0]] = holdings[syms[0]] - num_shares*2
                            Shares.append(num_shares*2)
                            Shares_all.append(-num_shares*2)

                        orders.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                        Date.append(normed.index[day])
                        Symbol.append(symbol_str)
                        Order.append("SELL")

                        orders_all.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                        Date_all.append(normed.index[day])
                        Symbol_all.append(symbol_str)
                        Order_all.append("SELL")
                elif (
                    (indicator_1[day] >= (self.threshold[2]))
                    and (indicator_1[day-1] < (self.threshold[2]))
                    and (-num_shares < holdings[syms[0]] <= num_shares)
                    and (-num_shares <= holdings[syms[0]] <= num_shares)
                ):  # crossed SMA upwards and hold long
                    # print ('3333 ')
                    if holdings[syms[0]] == 0:
                        holdings[syms[0]] = holdings[syms[0]] - num_shares
                        Shares.append(num_shares)
                        Shares_all.append(-num_shares)

                    else:
                        holdings[syms[0]] = holdings[syms[0]] - num_shares*2
                        Shares.append(num_shares*2)
                        Shares_all.append(-num_shares*2)

                    orders.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("SELL")

                    orders_all.append([normed.index[day].date(), syms[0], "SELL", num_shares])
                    Date_all.append(normed.index[day])
                    Symbol_all.append(symbol_str)
                    Order_all.append("SELL")


                elif (
                    (indicator_1[day] <= (self.threshold[0]))
                    and (indicator_1[day-1] > (self.threshold[0]))
                    and (-num_shares <= holdings[syms[0]] <= num_shares)
                ):  # crossed SMA downwards and hold short
                    # print '4444 '
                    if holdings[syms[0]] == 0:

                        holdings[syms[0]] = holdings[syms[0]] + num_shares
                        Shares.append(num_shares)
                        Shares_all.append(num_shares)
                    else:
                        holdings[syms[0]] = holdings[syms[0]] + num_shares*2
                        Shares.append(num_shares*2)
                        Shares_all.append(num_shares*2)


                    orders.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("BUY")

                    orders_all.append([normed.index[day].date(), syms[0], "BUY", num_shares])
                    Date_all.append(normed.index[day])
                    Symbol_all.append(symbol_str)
                    Order_all.append("BUY")  

                else:
                    Shares_all.append(0)
                    orders_all.append([normed.index[day].date(), syms[0], "HOLD", 0])
                    Date_all.append(normed.index[day])
                    Symbol_all.append(symbol_str)
                    Order_all.append("HOLD")                    

        # if (holdings[syms[0]] > 0):
        #     orders.append([ed, syms[0], "SELL", holdings[syms[0]]])
        #     Shares.append(holdings[syms[0]])
        #     Date.append(ed)
        #     Symbol.append(symbol_str)
        #     Order.append("SELL")

        #     orders_all[-1] = ([ed, syms[0], "SELL", holdings[syms[0]]])
        #     Shares_all[-1] = (-holdings[syms[0]])
        #     Date_all[-1] = (ed)
        #     Symbol_all[-1] = (symbol_str)
        #     Order_all[-1] = ("SELL")            

        df = pd.DataFrame({"Symbol": Symbol}, index=Date)
        df["Order"] = Order
        df["Shares"] = Shares
        self.num_order = df.shape[0]
        print("NUM ORDERS  ===============> ", self.num_order)

        df_all = pd.DataFrame({"Symbol": Symbol_all}, index=Date_all)
        df_all["Order"] = Order_all
        df_all["Shares"] = Shares_all
        return df, df_all



if __name__ == "__main__":
    print("One does not simply think up a strategy")
