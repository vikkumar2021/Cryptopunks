import datetime as dt
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as spo

# from marketsimcode import marketsim_df
import StrategyLearner as sl
from util import get_data, plot_data


def assess_porfolio(port_val):
    rfr = 0
    sf = 252
    cr = (port_val[-1] / port_val[0]) - 1
    daily_rets = (port_val / port_val.shift(1)) - 1
    daily_rets = daily_rets[1:]
    avg_daily_ret = daily_rets.mean()
    std_daily_ret = daily_rets.std()
    sharpe_ratio = np.sqrt(252) * daily_rets.mean() / std_daily_ret
    return cr, avg_daily_ret, std_daily_ret, sharpe_ratio


def benchmark(
    order=[],
    start_val=1000000,
    commission=9.95,
    impact=0.005,
    sd=dt.datetime(2010, 1, 1),
    ed=dt.datetime(2011, 12, 31),
):

    syms = order.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end
    dates = pd.date_range(sd, ed)
    df_prices_all = get_data(syms, dates, addSPY=False)  # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)
    # df_prices_SPY = df_prices_all['SPY']  # only SPY, for comparison later
    df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
    df_trade = df_trade.fillna(0)

    for i, row in order.iterrows():  # go through each order
        if row.Order == "BUY":
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] + row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                - (row.Shares * ((1 + impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                + (row.Shares * ((1 - impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
    # print df_trade
    df_holding = pd.DataFrame(index=df_prices.index, columns=cols)
    df_holding = df_holding.fillna(0)
    df_holding = df_trade.cumsum()
    df_holding["CASH"] = df_holding["CASH"] + start_val
    # print df_holding
    df_value = pd.DataFrame(index=df_prices.index, columns=cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]

    df_value["CASH"] = df_holding["CASH"]
    # print df_value
    portvals = df_value.sum(axis=1)
    return portvals


def get_manual(
    symbol="JPM",
    start_val=10000,
    commission=9.95,
    impact=0.005,
    sd=dt.datetime(2010, 1, 1),
    ed=dt.datetime(2011, 12, 31),
):

    start_date = sd
    end_date = ed
    syms = [symbol]
    allocations = [1.0]
    start_val = start_val
    risk_free_rate = 0.0
    sample_freq = 252

    lookback = 10
    dates = pd.date_range(start_date, end_date)
    prices_all = get_data(syms, dates, addSPY=False)
    prices = prices_all[syms]  # only portfolio symbols
    prices.fillna(method="ffill", inplace=True)
    prices.fillna(method="bfill", inplace=True)
    # prices_SPY = prices_all['SPY']  # only SPY, for comparison later
    normed = prices / prices.values[0, :]
    allocations = normed * allocations
    pos_vals = allocations * start_val
    port_val = pos_vals.sum(axis=1)
    prices_OURS_norm = port_val / port_val.values[0]
    daily_returns = (port_val / port_val.shift(1)) - 1
    daily_returns = daily_returns[1:]
    print("GET_MANUAL_STRATEGY ...")

    sma_ratio = prices.copy()
    sma = normed.cumsum()
    sma.values[lookback:, :] = (
        sma.values[lookback:, :] - sma.values[:-lookback, :]
    ) / lookback
    sma.ix[:lookback, :] = np.nan
    sma_ratio = normed / sma

    bbp = normed.copy()
    bottom_band = normed.copy()
    top_band = normed.copy()
    rolling_std = normed.rolling(window=lookback, min_periods=lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    bbp = (normed - bottom_band) / (top_band - bottom_band)

    rsi = normed.copy()
    for day in range(normed.shape[0]):
        for sym in syms:
            up_gain = 0
            down_loss = 0
            for prev_day in range(day - lookback + 1, day + 1):
                delta = normed.ix[prev_day, sym] - normed.ix[prev_day - 1, sym]
                if delta >= 0:
                    up_gain = up_gain + delta
                else:
                    down_loss = down_loss - delta
            if down_loss == 0:
                rsi.ix[day, sym] = 100
            else:
                rs = (up_gain / lookback) / (down_loss / lookback)
                rsi.ix[day, sym] = 100 - (100 / (1 + rs))

    threshold = [0.95, 0.3, 35, 1.05, 1, 65, 1, 1]
    Date = []
    Symbol = []
    Order = []
    Shares = []
    SELL = []
    BUY = []
    orders = []
    holdings = {sym: 0 for sym in syms}
    for day in range(lookback + 1, normed.shape[0]):

        if (
            (sma.ix[day, syms[0]] < threshold[0])
            and (bbp.ix[day, syms[0]] < threshold[1])
            and (rsi.ix[day, syms[0]] < threshold[2])
            and (-1000 <= holdings[syms[0]] < 1000)
        ):
            if holdings[syms[0]] < 1000:  # stock oversold but index is not oversold
                print("1111 ")
                if holdings[syms[0]] == 0:
                    holdings[syms[0]] = holdings[syms[0]] + 1000
                    Shares.append(1000)
                else:  # hold = -1000
                    holdings[syms[0]] = holdings[syms[0]] + 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), syms[0], "BUY", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol)
                Order.append("BUY")
        elif (
            (sma.ix[day, syms[0]] > threshold[3])
            and (bbp.ix[day, syms[0]] > threshold[4])
            and (rsi.ix[day, syms[0]] > threshold[5])
            and (-1000 <= holdings[syms[0]] <= 1000)
        ):  # stock overbought but index is not overbought
            if holdings[syms[0]] > -1000:
                print("2222 ")
                if holdings[syms[0]] == 0:
                    holdings[syms[0]] = holdings[syms[0]] - 1000
                    Shares.append(1000)
                else:
                    holdings[syms[0]] = holdings[syms[0]] - 2000
                    Shares.append(2000)

                orders.append([normed.index[day].date(), syms[0], "SELL", 1000])
                Date.append(normed.index[day])
                Symbol.append(symbol)
                Order.append("SELL")
        elif (
            (sma.ix[day, syms[0]] >= threshold[6])
            and (sma.ix[day - 1, syms[0]] < threshold[6])
            and (-1000 <= holdings[syms[0]] <= 1000)
        ):  # crossed SMA upwards and hold long
            if holdings[syms[0]] == 0:
                holdings[syms[0]] = holdings[syms[0]] - 1000
                Shares.append(1000)
                print("3333 ")
            else:
                holdings[syms[0]] = holdings[syms[0]] - 2000
                Shares.append(2000)
                print("3333 ")

            orders.append([normed.index[day].date(), syms[0], "SELL", 1000])
            Date.append(normed.index[day])
            Symbol.append(symbol)
            Order.append("SELL")
        elif (
            (sma.ix[day, syms[0]] <= threshold[7])
            and (sma.ix[day - 1, syms[0]] > threshold[7])
            and (-1000 <= holdings[syms[0]] < 1000)
        ):  # crossed SMA downwards and hold short
            if holdings[syms[0]] == 0:
                holdings[syms[0]] = holdings[syms[0]] + 1000
                Shares.append(1000)
                print("4444 ")
            else:
                holdings[syms[0]] = holdings[syms[0]] + 2000
                Shares.append(2000)
                print("4444 ")

            orders.append([normed.index[day].date(), syms[0], "BUY", 1000])
            Date.append(normed.index[day])
            Symbol.append(symbol)
            Order.append("BUY")

    df = pd.DataFrame({"Symbol": Symbol}, index=Date)
    df["Order"] = Order
    df["Shares"] = Shares

    order = df
    syms = order.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end
    sd = sma.index[0]  # 1st date in the order
    ed = sma.index[-1]  # last date in the order
    dates = pd.date_range(sd, ed)
    impact = 0
    commission = 0
    df_prices_all = get_data(syms, dates, addSPY=False)  # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)
    df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
    df_trade = df_trade.fillna(0)
    for i, row in order.iterrows():  # go through each order
        if row.Order == "BUY":
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] + row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                - (row.Shares * ((1 + impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                + (row.Shares * ((1 - impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
    df_holding = pd.DataFrame(index=df_prices.index, columns=cols)
    df_holding = df_holding.fillna(0)
    df_holding = df_trade.cumsum()
    # start_val = 10000
    df_holding["CASH"] = df_holding["CASH"] + start_val
    # print df_trade
    #    print 'holding < -1000', (df_holding[syms[0]]<-1000).any()
    #    print 'holding > 1000', (df_holding[syms[0]]>1000).any()
    df_value = pd.DataFrame(index=df_prices.index, columns=cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]
    df_value["CASH"] = df_holding["CASH"]
    portvals = df_value.sum(axis=1)

    return portvals


def marketsim(
    order=[],
    start_val=10000,
    commission=9.95,
    impact=0.005,
    sd=dt.datetime(2010, 1, 1),
    ed=dt.datetime(2011, 12, 31),
):

    #    order = pd.read_csv(orders_file, index_col='Date', parse_dates=True)
    #    order.sort_index
    syms = order.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end

    start_date = order.index[0]  # 1st date in the order
    end_date = order.index[-1]  # last date in the order
    #    start_date = dt.datetime(2010, 1, 1)
    #    end_date = dt.datetime(2011,12,31)
    dates = pd.date_range(sd, ed)

    print("\n**************   ")

    # STEP 1: df_prices, get adjusted close val from /data
    df_prices_all = get_data(syms, dates, addSPY=False)  # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)
    # df_prices_SPY = df_prices_all['SPY']  # only SPY, for comparison later

    df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
    df_trade = df_trade.fillna(0)

    for i, row in order.iterrows():  # go through each order
        if row.Order == "BUY":
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] + row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                - (row.Shares * ((1 + impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]["CASH"] = (
                df_trade.loc[i]["CASH"]
                + (row.Shares * ((1 - impact) * df_prices.loc[i][row.Symbol]))
                - (commission)
            )
    # print (df_trade)

    df_holding = pd.DataFrame(index=df_prices.index, columns=cols)
    df_holding = df_holding.fillna(0)
    df_holding = df_trade.cumsum()
    df_holding["CASH"] = df_holding["CASH"] + start_val
    # print (df_holding)
    # print ('holding < -1000', (df_holding[syms[0]]<-1000).any())
    # print ('holding > 1000', (df_holding[syms[0]]>1000).any())
    df_value = pd.DataFrame(index=df_prices.index, columns=cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]

    df_value["CASH"] = df_holding["CASH"]
    # print df_value

    portvals = df_value.sum(axis=1)
    # print portvals

    portvals_norm = portvals / portvals.values[0]
    Date = portvals.head(1).index

    df_benchmark = pd.DataFrame(index=Date)
    df_benchmark["Symbol"] = syms
    df_benchmark["Order"] = ["BUY"]
    df_benchmark["Shares"] = [1000]

    Date2 = portvals.tail(1).index
    dummy = pd.DataFrame(index=Date2)
    dummy["Symbol"] = syms
    dummy["Order"] = ["SELL"]
    dummy["Shares"] = [1000]

    # df_benchmark = df_benchmark.append(dummy)
    # print '555555555555555555555555555555', df_benchmark
    print("df_benchmark = ", df_benchmark)
    portvals_benchmark = benchmark(
        order=df_benchmark,
        start_val=start_val,
        commission=0.0,
        impact=0.0,
        sd=sd,
        ed=ed,
    )
    print("portvals_benchmark AFTER = ", portvals_benchmark)
    portvals_benchmark_norm = portvals_benchmark / portvals_benchmark.values[0]
    print("portvals_benchmark_norm = ", portvals_benchmark_norm)

    portvals_manual = get_manual(
        symbol=syms[0], start_val=start_val, commission=0, impact=0, sd=sd, ed=ed
    )
    portvals_manual_norm = portvals_manual / portvals_manual.values[0]

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_porfolio(
        port_val=portvals_benchmark
    )
    print("\n\n**********  BENCHMARK  **********")
    print(
        "last_day_portval = {}".format(portvals_benchmark[-1])
    )  # last value or portval
    print("sharpe_ratio = {}".format(sharpe_ratio))
    print("Cumulative return = {}".format(cum_ret))

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_porfolio(
        port_val=portvals_manual
    )
    print("\n**********  MANUAL STRATEGY  **********")
    print("last_day_portval = {}".format(portvals_manual[-1]))  # last value or portval
    print("sharpe_ratio = {}".format(sharpe_ratio))
    print("Cumulative return = {}".format(cum_ret))

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_porfolio(
        port_val=portvals
    )
    print("\n**********  OPTO LEARNER STRATEGY  **********")
    print("last_day_portval = {}".format(portvals[-1]))  # last value or portval
    print("sharpe_ratio = {}".format(sharpe_ratio))
    print("Cumulative return = {}".format(cum_ret))

    #    ********************  PLOT   *****************************
    plt.figure()
    # df_temp = pd.concat([portvals_benchmark, portvals_manual, portvals], keys=['portvals_benchmark','portvals_manual',  'portvals_opto'], axis=1)
    # aa = df_temp.plot(title='Benchmark vs Manual vs Optimization strategy portvals - IN SAMPLE', color = ['b','black', 'r'],label='benchmark')
    df_temp = pd.concat(
        [portvals_benchmark, portvals],
        keys=["portvals_benchmark", "portvals_opto"],
        axis=1,
    )
    aa = df_temp.plot(
        title="Benchmark vs Optimization strategy portvals - IN SAMPLE",
        color=["b", "r"],
        label="benchmark",
    )
    aa.set_xlabel("Date")
    aa.set_ylabel("Normalized portvals ")

    plt.grid()
    plt.show()
    #    **************************************************************

    return portvals
    print()


def plot_buy_sell(orders):
    symbol = ["BTC-USD"]
    sd = dt.datetime(2021, 4, 1)
    ed = dt.datetime(2021, 10, 1)

    sd = dt.datetime(2017, 3, 21)
    ed = dt.datetime(2022, 3, 21)

    dates = pd.date_range(sd, ed)
    prices_all = get_data(symbol, dates, addSPY=False)
    # print (prices_all)
    # prices = prices_all[symbol]
    # prices.fillna(method="ffill", inplace=True)
    # prices.fillna(method="bfill", inplace=True)
    # normed = prices/prices.values[0,:]
    # print (normed)

    aa = prices_all.plot()
    aa.set_xlabel("Date")
    aa.set_ylabel("BTC Price ")
    for i, row in orders.iterrows():
        if row.Order == "BUY":
            plt.axvline(x=i, color="green", ls=":", label="Buy")
        else:
            plt.axvline(x=i, color="red", ls=":", label="Sell")

    plt.grid()
    plt.legend()
    plt.title("BTC price, Buys and Sells Orders")
    plt.show()


def run_logic():

    # start_date_i = dt.datetime(2021, 4, 1)
    # end_date_i = dt.datetime(2021, 10, 1)
    start_date_i = dt.datetime(2017, 3, 21)
    end_date_i = dt.datetime(2022, 3, 21)
    symbol = "BTC-USD"  # "JPM"

    sv = 100000
    commission = 0.0
    impact = 0.0

    learner = sl.StrategyLearner(verbose=False, impact=impact)
    learner.addEvidence(symbol=symbol, sd=start_date_i, ed=end_date_i, sv=sv)

    df_trades = learner.testPolicy(symbol=symbol, sd=start_date_i, ed=end_date_i, sv=sv)
    print(df_trades)
    print("END TRADE")

    portvals_opto = marketsim(
        order=df_trades,
        start_val=sv,
        commission=commission,
        impact=impact,
        sd=start_date_i,
        ed=end_date_i,
    )

    print()

    plot_buy_sell(df_trades)
    return df_trades
