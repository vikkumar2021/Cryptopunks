import datetime as dt
from datetime import datetime
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as spo


# from marketsimcode import marketsim_df
import StrategyLearner_v2 as sl
from util import get_data, plot_data



def df_to_order(df, symbol, sd=dt.datetime(2014, 9, 20), ed=dt.datetime(2020, 12, 31)):
    df = df.reset_index()
    df = df.rename(columns={"index": "TradeDate"})
    df = df[df["Shares"] != 0]
    # df["Order"] = 0
    # df["Order"][df["Shares"] < 0] = "SELL"
    # df["Order"][df["Shares"] > 0] = "BUY"
    df["Symbol"] = symbol
    df["Shares"] = abs(df["Shares"])
    df = df.reset_index(drop=True)
    return df

def compute_portvals_2(orders_df, dataframebtc,  start_val=100000):
    syms = orders_df.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end
    start_date = orders_df.index[0]  # 1st date in the order
    end_date = orders_df.index[-1]  # last date in the order
    dates = pd.date_range(start_date, end_date)
    df_prices_all = dataframebtc
    df_prices = df_prices_all[['Adj_Close']]
    df_prices = df_prices.rename(columns={"Adj_Close": 'BTC'})
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)

    df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
    df_trade = df_trade.fillna(0)

    commission = 0
    impact = 0
    for i, row in orders_df.iterrows():  # go through each order
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
    df_holding["CASH"] = df_holding["CASH"] + start_val
    #print ('\ndf_holding = ', df_holding)
    df_value = pd.DataFrame(index=df_prices.index, columns=cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]

    df_value["CASH"] = df_holding["CASH"]
    #print ('\ndf_value', df_value)

    portvals = df_value.sum(axis=1)
    #print ('\nportvals = ', portvals)
    portval1_df = pd.DataFrame(portvals)
    portval1_df = portval1_df.reset_index()
    portval1_df = portval1_df.rename(columns = {"index":"TradeDate", 0:'value'})
    return portval1_df


def run_logic(config, dataframebtc_input):

    symbol = config.get("ticker", "BTC")
    sd = datetime.strptime(config.get("training_sd"), "%Y-%m-%d")
    ed = datetime.strptime(config.get("training_ed"), "%Y-%m-%d")
    sd2 = datetime.strptime(config.get("test_sd"), "%Y-%m-%d")
    ed2 = datetime.strptime(config.get("test_ed"), "%Y-%m-%d")
    sv = int(config.get("sv", 1000000))

    alpha = float(config.get("alpha", 0.1))
    gamma = float(config.get("gamma", 0.9))
    rar = float(config.get("rar", 0.99))
    radr = float(config.get("radr", 0.8))        

    dates = pd.date_range(sd, ed)
    dataframebtc = pd.DataFrame(index=dates)
    dataframebtc = dataframebtc.join(dataframebtc_input)

    learner = sl.StrategyLearner(verbose=False, impact=0)
    learner.addEvidence(input_df=dataframebtc, symbol=symbol, sd=sd, ed=ed, sv=sv)
    df_trades = learner.testPolicy(input_df=dataframebtc, symbol=symbol, sd=sd, ed=ed, sv=sv)
    print('df_trade = ' , df_trades)
    print("END TRADE")

    # TRAIN - IM SAMPLE 
    portval1_df = compute_portvals_2(df_trades, dataframebtc_input,  start_val=100000)
    portval1_df = portval1_df.rename(columns={"value": "TrainGridSearch"})
    df2order = df_to_order(df=df_trades, symbol=symbol, sd=sd, ed=ed)
    df2order = df2order[["TradeDate", "Order"]]
    df2order = df2order.rename(columns={"Order": "TraingOrders"})

    order = [
        (
            sd,
            math.floor(sv / dataframebtc.loc[sd]["Adj_Close"]),
            "BUY",
            symbol,
        ),
        (
            ed,
            math.floor(sv / dataframebtc.loc[sd]["Adj_Close"]),
            "SELL",
            symbol,
        ),
    ]

    dfbench = pd.DataFrame(order, columns=["TradeDate", "Shares", "Order", "Symbol"])
    dfbench = dfbench.set_index('TradeDate')
    benchmark1 = compute_portvals_2(dfbench, dataframebtc_input,  start_val=100000)
    benchmark1 = benchmark1.rename(columns={"value": "TrainBenchmark"})


    df = dataframebtc_input.reset_index()
    df = df.rename(columns={"index": "TradeDate"})

    dataframebtccopia = df.copy()
    dataframebtccopia = dataframebtccopia.merge(df2order, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(portval1_df, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(benchmark1, on="TradeDate", how="left")


    # TEST - OUT SAMPLE
    sd2 = datetime.strptime(config.get("test_sd"), "%Y-%m-%d")
    ed2 = datetime.strptime(config.get("test_ed"), "%Y-%m-%d")
    sv = int(config.get("sv", 1000000))

    dates = pd.date_range(sd2, ed2)
    dataframebtc2 = pd.DataFrame(index=dates)
    dataframebtc2 = dataframebtc2.join(dataframebtc_input)
    df_trades2 = learner.testPolicy(input_df=dataframebtc2, symbol=symbol, sd=sd2, ed=ed2, sv=sv)

    portval2_df = compute_portvals_2(df_trades2, dataframebtc_input,  start_val=100000)
    portval2_df = portval2_df.rename(columns={"value": "TestGridSearch"})
    df2order2 = df_to_order(df=df_trades2, symbol=symbol, sd=sd, ed=ed)
    df2order2 = df2order2[["TradeDate", "Order"]]
    df2order2 = df2order2.rename(columns={"Order": "TestOrders"})

    order2 = [
        (
            sd2,
            math.floor(sv / dataframebtc2.loc[sd2]["Adj_Close"]),
            "BUY",
            symbol,
        ),
        (
            ed2,
            math.floor(sv / dataframebtc2.loc[sd2]["Adj_Close"]),
            "SELL",
            symbol,
        ),
    ]


    dfbench2 = pd.DataFrame(order2, columns=["TradeDate", "Shares", "Order", "Symbol"])
    dfbench2 = dfbench2.set_index('TradeDate')
    benchmark2 = compute_portvals_2(dfbench2, dataframebtc_input,  start_val=100000)
    benchmark2 = benchmark2.rename(columns={"value": "TestBenchmark"})

    dataframebtccopia = dataframebtccopia.merge(df2order2, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(portval2_df, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(benchmark2, on="TradeDate", how="left")

    return dataframebtccopia
