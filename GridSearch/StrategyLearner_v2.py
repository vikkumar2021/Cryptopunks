# Minh Trang NGUYEN
# mnguyen306

import datetime as dt
import random

import numpy as np
import pandas as pd
import scipy.optimize as spo
from .marketsimcode import marketsim_df
from .util import get_data


def get_sharpe_ratio(threshold, *params):

    # print ('threshold in get_sharpe_ratio = ', threshold)
    # print ('len params = ', len(params))

    sma, bbp, rsi, normed, symbol_str, impact = params

    Date = []
    Symbol = []
    Order = []
    Shares = []
    SELL = []
    BUY = []
    orders = []
    syms = [symbol_str]
    holdings = {sym: 0 for sym in syms}
    lookback = 10
    num_order = 0
    for day in range(lookback + 1, normed.shape[0]):

        if (
            (sma.loc[day, syms[0]] < threshold[0])
            and (bbp.loc[day, syms[0]] < threshold[1])
            and (rsi.loc[day, syms[0]] < 100 * threshold[1])
            and (-1000 <= holdings[syms[0]] < 1000)
        ):
            if holdings[syms[0]] < 1000:  # stock oversold but index is not oversold
                # print ('1111 ')
                if holdings[syms[0]] == 0:
                    holdings[syms[0]] = holdings[syms[0]] + 1000
                    Shares.append(1000)
                else:  # hold = -1000
                    holdings[syms[0]] = holdings[syms[0]] + 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), syms[0], "BUY", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("BUY")
        elif (
            (sma.loc[day, syms[0]] > threshold[2])
            and (bbp.loc[day, syms[0]] > threshold[3])
            and (rsi.loc[day, syms[0]] > 100 * threshold[3])
            and (-1000 <= holdings[syms[0]] <= 1000)
        ):  # stock overbought but index is not overbought
            if holdings[syms[0]] > -1000:
                # print ('2222 ')
                if holdings[syms[0]] == 0:
                    holdings[syms[0]] = holdings[syms[0]] - 1000
                    Shares.append(1000)
                else:
                    holdings[syms[0]] = holdings[syms[0]] - 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), syms[0], "SELL", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("SELL")
        elif (
            (sma.loc[day, syms[0]] >= (threshold[2]))
            and (sma.loc[day - 1, syms[0]] < (threshold[2]))
            and (-1000 < holdings[syms[0]] <= 1000)
            and (-1000 <= holdings[syms[0]] <= 1000)
        ):  # crossed SMA upwards and hold long
            # print ('3333 ')
            if holdings[syms[0]] == 0:
                holdings[syms[0]] = holdings[syms[0]] - 1000
                Shares.append(1000)

            else:
                holdings[syms[0]] = holdings[syms[0]] - 2000
                Shares.append(2000)

            orders.append([normed.index[day].date(), syms[0], "SELL", 1000])
            Date.append(normed.index[day])
            Symbol.append(symbol_str)
            Order.append("SELL")
        elif (
            (sma.loc[day, syms[0]] <= (threshold[0]))
            and (sma.loc[day - 1, syms[0]] > (threshold[0]))
            and (-1000 <= holdings[syms[0]] < 1000)
        ):  # crossed SMA downwards and hold short
            # print '4444 '
            if holdings[syms[0]] == 0:

                holdings[syms[0]] = holdings[syms[0]] + 1000
                Shares.append(1000)
            else:
                holdings[syms[0]] = holdings[syms[0]] + 2000
                Shares.append(2000)

            orders.append([normed.index[day].date(), syms[0], "BUY", 1000])
            Date.append(normed.index[day])
            Symbol.append(symbol_str)
            Order.append("BUY")

    #    print "NUM ORDERS => ", len(Order)
    if len(Order) == 0:
        return 1000

    df = pd.DataFrame({"Symbol": Symbol}, index=Date)
    df["Order"] = Order
    df["Shares"] = Shares

    order = df
    syms = order.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end

    sd = sma.index[0]
    ed = sma.index[-1]
    dates = pd.date_range(sd, ed)

    commission = 0
    df_prices_all = get_data(syms, dates, addSPY=False)  # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols
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
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                - (row.Shares * ((1 + impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
            # df_trade.loc[i,row.Symbol] += row.Shares
            # df_trade.loc[i, 'CASH'] -= (row.Shares * ((1+impact)*df_prices.loc[i,row.Symbol])) - (commission)
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                + (row.Shares * ((1 - impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
            # df_trade.loc[i,row.Symbol] -= row.Shares
            # df_trade.loc[i,'CASH'] +=(row.Shares * ((1-impact)*df_prices.loc[i,row.Symbol])) - (commission)
    df_holding = pd.DataFrame(index=df_prices.index, columns=cols)
    df_holding = df_holding.fillna(0)
    df_holding = df_trade.cumsum()
    start_val = 10000
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
    rfr = 0
    sf = 252
    cr = (portvals[-1] / portvals[0]) - 1
    # print("TH , last day portval = ", threshold, portvals[-1])
    # print("ORDERS = ", Order)
    return -portvals[-1]
    return (-1) * cr
    daily_rets = (portvals / portvals.shift(1)) - 1
    daily_rets = daily_rets[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret

    print(-1) * sharpe_ratio
    return (-1) * sharpe_ratio
    # return '123456789'


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
    ):

        risk_free_rate = 0.0
        sample_freq = 252
        lookback = 10
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
            "********************* Add Evidence Computing SMA  ************************"
        )
        sma_ratio = prices.copy()
        sma = normed.cumsum()
        sma.values[lookback:, :] = (
            sma.values[lookback:, :] - sma.values[:-lookback, :]
        ) / lookback
        sma.iloc[:lookback, :] = np.nan
        sma_ratio = normed / sma

        print(
            "********************* Add Evidence Computing Bollinger Bands  ************************"
        )
        bbp = normed.copy()
        bottom_band = normed.copy()
        top_band = normed.copy()
        rolling_std = normed.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + (2 * rolling_std)
        bottom_band = sma - (2 * rolling_std)
        bbp = (normed - bottom_band) / (top_band - bottom_band)

        print(
            "********************* Add Evidence Computing RSI  ************************"
        )
        rsi = normed.copy()
        for day in range(normed.shape[0]):
            for sym in symbol:
                up_gain = 0
                down_loss = 0
                for prev_day in range(day - lookback + 1, day + 1):
                    delta = normed.loc[prev_day, sym] - normed.loc[prev_day - 1, sym]
                    if delta >= 0:
                        up_gain = up_gain + delta
                    else:
                        down_loss = down_loss - delta
                if down_loss == 0:
                    rsi.loc[day, sym] = 100
                else:
                    rs = (up_gain / lookback) / (down_loss / lookback)
                    rsi.loc[day, sym] = 100 - (100 / (1 + rs))

        # initial_threshold =[0.95, 0.3, 35, 1.05, 1, 65, 1, 1]
        initial_threshold = [0.95, 0.3, 1.05, 1]
        params = (sma_ratio, bbp, rsi, normed, symbol_str, self.impact)
        # aaa = get_sharpe_ratio(initial_threshold, *params)
        # print 'aaa  -->  '  , aaa

        rranges_old = [
            slice(0.54, 1.1, 0.2),  # BUY SMA 0.44 0.64 0.84 1.04
            slice(0.2, 0.41, 0.2),  # BUY BBP-RSI   0.2 0.4
            slice(0.55, 1.11, 0.3),  # SELL SMA  0.55 0.85 1.15
            slice(0.58, 0.81, 0.2),
        ]  # SELL BBP-RSI  0.58, 0.78
        print("\n\n\n HERE ----> ", min(sma_ratio))
        rranges = [
            slice(0.6, 1.01, 0.4),  #  SMA  RATIO
            slice(-0.2, 1.21, 0.4),  # BUY
            slice(1.0, 1.61, 0.4),  # SELL SMA
            slice(-0.2, 1.21, 0.4),
        ]  #  SELL BBP-RSI

        #    print rranges
        #    print len(rranges)
        #    print len(initial_threshold)
        threshold_brute = spo.brute(
            get_sharpe_ratio, rranges, args=params, full_output=True, finish=None
        )

        # self.threshold  = initial_threshold
        self.threshold = threshold_brute[0]
        print("========  self.threshold  ==========  ", self.threshold)

    def testPolicy(
        self,
        input_df,
        symbol="JPM",
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=100000,
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

        print(
            "********************* Test Policy Computing SMA  ************************"
        )
        sma_ratio = prices.copy()
        sma = normed.cumsum()
        sma.values[lookback:, :] = (
            sma.values[lookback:, :] - sma.values[:-lookback, :]
        ) / lookback
        sma.loc[:lookback, :] = np.nan
        # sma_ratio = normed/sma
        sma = normed / sma

        print(
            "********************* Test Policy Computing Bollinger Bands  ************************"
        )
        bbp = normed.copy()
        bottom_band = normed.copy()
        top_band = normed.copy()
        rolling_std = normed.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + (2 * rolling_std)
        bottom_band = sma - (2 * rolling_std)
        bbp = (normed - bottom_band) / (top_band - bottom_band)

        print(
            "********************* Test Policy Computing RSI  ************************"
        )
        rsi = normed.copy()
        for day in range(normed.shape[0]):
            for sym in symbol:
                up_gain = 0
                down_loss = 0
                for prev_day in range(day - lookback + 1, day + 1):
                    delta = normed.loc[prev_day, sym] - normed.loc[prev_day - 1, sym]
                    if delta >= 0:
                        up_gain = up_gain + delta
                    else:
                        down_loss = down_loss - delta
                if down_loss == 0:
                    rsi.loc[day, sym] = 100
                else:
                    rs = (up_gain / lookback) / (down_loss / lookback)
                    rsi.loc[day, sym] = 100 - (100 / (1 + rs))

        Date = []
        Symbol = []
        Order = []
        Shares = []
        SELL = []
        BUY = []
        orders = []
        holdings = {sym: 0 for sym in symbol}
        for day in range(lookback + 1, normed.shape[0]):

            if (
                (sma.loc[day, sym] < self.threshold[0])
                and (bbp.loc[day, sym] < self.threshold[1])
                and (rsi.loc[day, sym] < 100 * self.threshold[1])
            ):
                if holdings[sym] < 1000:  # stock oversold but index is not oversold
                    if holdings[sym] == 0:
                        holdings[sym] = holdings[sym] + 1000
                        Shares.append(1000)
                    else:
                        holdings[sym] = holdings[sym] + 2000
                        Shares.append(2000)

                    orders.append([normed.index[day].date(), sym, "BUY", 1000])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("BUY")
                    print("RULE 1, BUY at ", normed.index[day], holdings[sym])

            elif (
                (sma.loc[day, sym] > self.threshold[2])
                and (bbp.loc[day, sym] > self.threshold[3])
                and (rsi.loc[day, sym] > 100 * self.threshold[3])
            ):  # stock overbought but index is not overbought
                if holdings[sym] > -1000:
                    if holdings[sym] == 0:
                        holdings[sym] = holdings[sym] - 1000
                        Shares.append(1000)
                    else:
                        holdings[sym] = holdings[sym] - 2000
                        Shares.append(2000)

                    orders.append([normed.index[day].date(), sym, "SELL", 1000])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("SELL")

                    print("RULE 2, SELL at ", normed.index[day], holdings[sym])
            elif (
                (sma.loc[day, sym] >= (self.threshold[2]))
                and (sma.loc[day - 1, sym] < (self.threshold[2]))
                and (-1000 < holdings[sym] <= 1000)
            ):  # crossed SMA upwards and hold long
                if holdings[sym] == 0:
                    holdings[sym] = holdings[sym] - 1000
                    Shares.append(1000)
                else:
                    holdings[sym] = holdings[sym] - 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), sym, "SELL", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("SELL")

                print("RULE 3, SELL at ", normed.index[day], holdings[sym])
            elif (
                (sma.loc[day, sym] <= (self.threshold[0]))
                and (sma.loc[day - 1, sym] > (self.threshold[0]))
                and (-1000 <= holdings[sym] < 1000)
            ):  # crossed SMA downwards and hold short
                if holdings[sym] == 0:
                    holdings[sym] = holdings[sym] + 1000
                    Shares.append(1000)
                else:
                    holdings[sym] = holdings[sym] + 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), sym, "BUY", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("BUY")

                print("RULE 4, BUY at ", normed.index[day], holdings[sym])
        df = pd.DataFrame({"Symbol": Symbol}, index=Date)
        df["Order"] = Order
        df["Shares"] = Shares
        print("NUM ORDERS  ===============> ", df.shape)
        self.num_order = df.shape[0]
        print("NUM ORDERS  ===============> ", self.num_order)
        return df

    def testPolicy_old(
        self,
        symbol="JPM",
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv=100000,
    ):

        risk_free_rate = 0.0
        sample_freq = 252
        lookback = 10
        symbol_str = symbol
        symbol = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = get_data(symbol, dates, addSPY=False)
        prices = prices_all[symbol]
        prices.fillna(method="ffill", inplace=True)
        prices.fillna(method="bfill", inplace=True)
        normed = prices / prices.values[0, :]
        pos_vals = normed * sv
        port_val = pos_vals.sum(axis=1)
        prices_OURS_norm = port_val / port_val.values[0]
        daily_returns = (port_val / port_val.shift(1)) - 1
        daily_returns = daily_returns[1:]

        print(
            "********************* Test Policy Computing SMA  ************************"
        )
        sma_ratio = prices.copy()
        sma = normed.cumsum()
        sma.values[lookback:, :] = (
            sma.values[lookback:, :] - sma.values[:-lookback, :]
        ) / lookback
        sma.loc[:lookback, :] = np.nan
        sma_ratio = normed / sma

        print(
            "********************* Test Policy Computing Bollinger Bands  ************************"
        )
        bbp = normed.copy()
        bottom_band = normed.copy()
        top_band = normed.copy()
        rolling_std = normed.rolling(window=lookback, min_periods=lookback).std()
        top_band = sma + (2 * rolling_std)
        bottom_band = sma - (2 * rolling_std)
        bbp = (normed - bottom_band) / (top_band - bottom_band)

        print(
            "********************* Test Policy Computing RSI  ************************"
        )
        rsi = normed.copy()
        for day in range(normed.shape[0]):
            for sym in symbol:
                up_gain = 0
                down_loss = 0
                for prev_day in range(day - lookback + 1, day + 1):
                    delta = normed.loc[prev_day, sym] - normed.loc[prev_day - 1, sym]
                    if delta >= 0:
                        up_gain = up_gain + delta
                    else:
                        down_loss = down_loss - delta
                if down_loss == 0:
                    rsi.loc[day, sym] = 100
                else:
                    rs = (up_gain / lookback) / (down_loss / lookback)
                    rsi.loc[day, sym] = 100 - (100 / (1 + rs))

        Date = []
        Symbol = []
        Order = []
        Shares = []
        SELL = []
        BUY = []
        orders = []
        holdings = {sym: 0 for sym in symbol}
        for day in range(lookback + 1, normed.shape[0]):

            if (
                (sma.loc[day, sym] < self.threshold[0])
                and (bbp.loc[day, sym] < self.threshold[1])
                and (rsi.loc[day, sym] < 100 * self.threshold[1])
            ):
                if holdings[sym] < 1000:  # stock oversold but index is not oversold
                    if holdings[sym] == 0:
                        holdings[sym] = holdings[sym] + 1000
                        Shares.append(1000)
                    else:
                        holdings[sym] = holdings[sym] + 2000
                        Shares.append(2000)

                    orders.append([normed.index[day].date(), sym, "BUY", 1000])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("BUY")
                    print("RULE 1, BUY at ", normed.index[day], holdings[sym])

            elif (
                (sma.loc[day, sym] > self.threshold[2])
                and (bbp.loc[day, sym] > self.threshold[3])
                and (rsi.loc[day, sym] > 100 * self.threshold[3])
            ):  # stock overbought but index is not overbought
                if holdings[sym] > -1000:
                    if holdings[sym] == 0:
                        holdings[sym] = holdings[sym] - 1000
                        Shares.append(1000)
                    else:
                        holdings[sym] = holdings[sym] - 2000
                        Shares.append(2000)

                    orders.append([normed.index[day].date(), sym, "SELL", 1000])
                    Date.append(normed.index[day])
                    Symbol.append(symbol_str)
                    Order.append("SELL")

                    print("RULE 2, SELL at ", normed.index[day], holdings[sym])
            elif (
                (sma.loc[day, sym] >= (self.threshold[2] - 0.05))
                and (sma.loc[day - 1, sym] < (self.threshold[2] - 0.05))
                and (-1000 < holdings[sym] <= 1000)
            ):  # crossed SMA upwards and hold long
                if holdings[sym] == 0:
                    holdings[sym] = holdings[sym] - 1000
                    Shares.append(1000)
                else:
                    holdings[sym] = holdings[sym] - 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), sym, "SELL", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("SELL")

                print("RULE 3, SELL at ", normed.index[day], holdings[sym])
            elif (
                (sma.loc[day, sym] <= (self.threshold[0] + 0.05))
                and (sma.loc[day - 1, sym] > (self.threshold[0] + 0.05))
                and (-1000 <= holdings[sym] < 1000)
            ):  # crossed SMA downwards and hold short
                if holdings[sym] == 0:
                    holdings[sym] = holdings[sym] + 1000
                    Shares.append(1000)
                else:
                    holdings[sym] = holdings[sym] + 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), sym, "BUY", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol_str)
                Order.append("BUY")

                print("RULE 4, BUY at ", normed.index[day], holdings[sym])
        df = pd.DataFrame({"Symbol": Symbol}, index=Date)
        df["Order"] = Order
        df["Shares"] = Shares
        print("NUM ORDERS  ===============> ", df.shape)
        self.num_order = df.shape[0]
        print("NUM ORDERS  ===============> ", self.num_order)
        return df


if __name__ == "__main__":
    print("One does not simply think up a strategy")
