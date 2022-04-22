import datetime as dt
from datetime import datetime
import math
import pandas as pd


from . import StrategyLearner_v2 as sl


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


def compute_portvals_2(orders_df, dataframebtc, start_val=100000):
    syms = orders_df.Symbol.unique()  # find unique symbols
    syms = syms.tolist()
    cols = syms + ["CASH"]  # add a column CASH at the end

    df_prices_all = dataframebtc
    df_prices = df_prices_all[["Adj_Close"]]
    df_prices = df_prices.rename(columns={"Adj_Close": "BTC"})
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)   

    if len(orders_df["Order"]) == 0:
        df_trade = pd.DataFrame(index=df_prices.index, columns=cols)
        df_trade = df_trade.fillna(0)
        df_trade['value'] =start_val
        portval1_df = df_trade.reset_index()
        portval1_df = df_trade.rename(columns={"index": "TradeDate", 0: "value"})
        return portval1_df
    else:
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
        # print ('\ndf_holding = ', df_holding)
        df_value = pd.DataFrame(index=df_prices.index, columns=cols)
        for i, row in df_holding.iterrows():
            for sym in syms:
                df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]

        df_value["CASH"] = df_holding["CASH"]
        # print ('\ndf_value', df_value)

        portvals = df_value.sum(axis=1)
        # print ('\nportvals = ', portvals)
        portval1_df = pd.DataFrame(portvals)
        portval1_df = portval1_df.reset_index()
        portval1_df = portval1_df.rename(columns={"index": "TradeDate", 0: "value"})

        return portval1_df


def run_logic(config, dataframebtc_input):

    symbol = config.get("ticker", "BTC")
    sd = datetime.strptime(config.get("training_sd"), "%Y-%m-%d")
    sd_raw = config.get("training_sd")
    ed = datetime.strptime(config.get("training_ed"), "%Y-%m-%d")
    sd2 = datetime.strptime(config.get("test_sd"), "%Y-%m-%d")
    sd_raw2 = config.get("test_sd")
    ed2 = datetime.strptime(config.get("test_ed"), "%Y-%m-%d")
    sv = int(config.get("sv", 1000000))

    alpha = float(config.get("alpha", 0.1))
    gamma = float(config.get("gamma", 0.9))
    rar = float(config.get("rar", 0.99))
    radr = float(config.get("radr", 0.8))

    dates = pd.date_range(sd, ed)
    dataframebtc = pd.DataFrame(index=dates)
    df_indexDate = dataframebtc_input.set_index('TradeDate')

    dataframebtc = dataframebtc.join(df_indexDate)
    learner = sl.StrategyLearner(verbose=False, impact=0)

    # BENCHMARK - IM SAMPLE
    num_shares = math.floor(sv / dataframebtc_input["Adj_Close"][dataframebtc_input["TradeDate"] == sd])
    order = [
        (
            sd,
            num_shares,
            "BUY",
            symbol,
        ),
        (
            ed,
            num_shares,
            "SELL",
            symbol,
        ),
    ]

    dfbench = pd.DataFrame(order, columns=["TradeDate", "Shares", "Order", "Symbol"])
    dfbench = dfbench.set_index("TradeDate")
    benchmark1 = compute_portvals_2(dfbench, df_indexDate, start_val=sv)
    benchmark1 = benchmark1.rename(columns={"value": "TrainBenchmark"})

    learner.addEvidence(input_df=dataframebtc, symbol=symbol, sd=sd, ed=ed, sv=sv, num_shares=num_shares)
    df_trades = learner.testPolicy(
        input_df=dataframebtc, symbol=symbol, sd=sd, ed=ed, sv=sv, num_shares=num_shares
    )
    print("df_trade = ", df_trades)
    print("END TRADE")

    # TRAIN - IM SAMPLE
    portval1_df = compute_portvals_2(df_trades, df_indexDate, start_val=sv)
    portval1_df = portval1_df.rename(columns={"value": "TrainGridSearch"})
    df2order = df_to_order(df=df_trades, symbol=symbol, sd=sd, ed=ed)
    df2order = df2order[["TradeDate", "Order"]]
    df2order = df2order.rename(columns={"Order": "TraingOrders"})


    df = dataframebtc_input.reset_index()
    df = df.rename(columns={"index": "TradeDate"})

    dataframebtccopia = dataframebtc_input.copy()
    print ('\nDEBUG df2order = ', df2order.head())
    print ('\nDEBUG dataframebtccopia = ', dataframebtccopia.head())
    dataframebtccopia = dataframebtccopia.merge(df2order, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(portval1_df, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(benchmark1, on="TradeDate", how="left")

    # BENCH - OUT OF  SAMPLE
    num_shares2 = math.floor(sv / dataframebtc_input["Adj_Close"][dataframebtc_input["TradeDate"] == sd2])
    order2 = [
        (
            sd2,
            num_shares2,
            "BUY",
            symbol,
        ),
        (
            ed2,
            num_shares2,
            "SELL",
            symbol,
        ),
    ]

    dfbench2 = pd.DataFrame(order2, columns=["TradeDate", "Shares", "Order", "Symbol"])
    dfbench2 = dfbench2.set_index("TradeDate")
    benchmark2 = compute_portvals_2(dfbench2, df_indexDate, start_val=sv)
    benchmark2 = benchmark2.rename(columns={"value": "TestBenchmark"})


    # TEST - OUT SAMPLE
    sd2 = datetime.strptime(config.get("test_sd"), "%Y-%m-%d")
    ed2 = datetime.strptime(config.get("test_ed"), "%Y-%m-%d")
    sv = int(config.get("sv", 1000000))

    dates = pd.date_range(sd2, ed2)
    dataframebtc2 = pd.DataFrame(index=dates)
    dataframebtc2 = dataframebtc2.join(df_indexDate)
  
    df_trades2 = learner.testPolicy(
        input_df=dataframebtc2, symbol=symbol, sd=sd2, ed=ed2, sv=sv, num_shares=num_shares2
    )

    portval2_df = compute_portvals_2(df_trades2, df_indexDate, start_val=sv)
    portval2_df = portval2_df.rename(columns={"value": "TestGridSearch"})
    df2order2 = df_to_order(df=df_trades2, symbol=symbol, sd=sd, ed=ed)
    df2order2 = df2order2[["TradeDate", "Order"]]
    df2order2 = df2order2.rename(columns={"Order": "TestOrders"})


    dataframebtccopia = dataframebtccopia.merge(df2order2, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(portval2_df, on="TradeDate", how="left")
    dataframebtccopia = dataframebtccopia.merge(benchmark2, on="TradeDate", how="left")
    dataframebtccopia['TradeDate'] = dataframebtccopia["TradeDate"].dt.strftime('%Y-%m-%d')

    return dataframebtccopia
