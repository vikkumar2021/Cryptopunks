"""MLT: Utility code."""

import os
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def symbol_to_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol."""
    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", "../data/")
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data_old(symbols, dates, addSPY=True, colname="Adj Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if addSPY and "SPY" not in symbols:  # add SPY for reference, if absent
        symbols = ["SPY"] + symbols

    for symbol in symbols:
        df_temp = pd.read_csv(
            symbol_to_path(symbol),
            index_col="Date",
            parse_dates=True,
            usecols=["Date", colname],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)
        if symbol == "SPY":  # drop dates SPY did not trade
            df = df.dropna(subset=["SPY"])

    return df


def get_data(symbols, dates, addSPY=True, colname="Adj_Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    for symbol in symbols:
        df_temp = pd.read_csv(
            "pipeline.csv",
            index_col="TradeDate",
            parse_dates=True,
            usecols=["TradeDate", colname],
            na_values=["nan"],
        )
        df_temp = df_temp.rename(columns={colname: symbol})
        df = df.join(df_temp)

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price", colors="b"):
    import matplotlib.pyplot as plt

    """Plot stock prices with a custom title and meaningful axis labels."""
    # print df.head()
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.grid()
    plt.show()


def get_orders_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("ORDERS_DATA_DIR", "orders/"), basefilename)
    )


def get_learner_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("LEARNER_DATA_DIR", "Data/"), basefilename), "r"
    )


def get_robot_world_file(basefilename):
    return open(
        os.path.join(os.environ.get("ROBOT_WORLDS_DIR", "testworlds/"), basefilename)
    )


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


def compute_portvals(orders_df, start_val=100000):
    start = orders_df.loc[0]["TradeDate"]
    end = orders_df.loc[len(orders_df) - 1]["TradeDate"]

    tickers = orders_df["Symbol"].unique()

    port_vals = get_data([tickers[0]], pd.date_range(start, end), addSPY=False)
    port_vals["Cash"] = 1

    trades_df = port_vals.copy()

    for col in trades_df.columns:
        trades_df[col] = float(0)

    symbol = "Adj_Close"
    for i in range(len(orders_df)):
        d = orders_df.loc[i]["TradeDate"]
        amount = orders_df.loc[i]["Shares"]
        if orders_df.loc[i]["Order"] == "BUY":
            sign = 1
        elif orders_df.loc[i]["Order"] == "SELL":
            sign = -1

        trades_df[symbol][d] = trades_df[symbol][d] + sign * amount

    cost_df = port_vals * trades_df
    # print(cost_df.head)

    trades_df["Cash"] = -1 * cost_df.sum(axis=1)
    # print(trades_df.head)

    holdings_df = port_vals.copy()
    for col in trades_df.columns:
        holdings_df[col] = 0

    dates = holdings_df.index
    holdings_df = holdings_df.reset_index(drop=True).copy()
    trades_df2 = trades_df.reset_index(drop=True).copy()

    for i in range(len(holdings_df)):
        if i == 0:
            holdings_df.loc[i] = trades_df2.loc[i]
            holdings_df.loc[i]["Cash"] = start_val + trades_df2.loc[i]["Cash"]
        else:
            holdings_df.loc[i] = holdings_df.loc[i - 1] + trades_df2.loc[i]

    holdings_df["TradeDate"] = dates
    holdings_df = holdings_df.set_index("TradeDate")
    # print(holdings_df)

    vals = port_vals * holdings_df
    # print(vals.head)
    vals_sum = pd.DataFrame(vals.sum(axis=1), columns=["Sum"])
    # print(vals_sum.head)
    return vals_sum
