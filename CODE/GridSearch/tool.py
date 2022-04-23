import datetime as dt
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.optimize as spo
import StrategyLearner as sl
from marketsimcode import marketsim_df
from util import get_data, plot_data


def marketsim(order = [], start_val = 10000, commission=9.95, impact=0.005, sd = dt.datetime(2010, 1, 1), ed = dt.datetime(2011, 12, 31)):

    
#    order = pd.read_csv(orders_file, index_col='Date', parse_dates=True)
#    order.sort_index
    syms = order.Symbol.unique() # find unique symbols
    syms = syms.tolist()
    cols = syms + ['CASH']   # add a column CASH at the end 

    start_date = order.index[0] # 1st date in the order
    end_date = order.index[-1] # last date in the order
#    start_date = dt.datetime(2010, 1, 1)
#    end_date = dt.datetime(2011,12,31)
    dates = pd.date_range(sd, ed)

    print '\n**************   '

    
    # STEP 1: df_prices, get adjusted close val from /data
    df_prices_all = get_data(syms, dates) # automatically adds SPY
    df_prices = df_prices_all[syms]  # only portfolio symbols
    df_prices.fillna(method="ffill", inplace=True)
    df_prices.fillna(method="bfill", inplace=True)
    df_prices_SPY = df_prices_all['SPY']  # only SPY, for comparison later

    df_trade = pd.DataFrame(index=df_prices.index, columns = cols)
    df_trade=df_trade.fillna(0)
    
    for i, row in order.iterrows(): # go through each order
        if (row.Order == "BUY"):
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] + row.Shares
            df_trade.loc[i]['CASH'] = df_trade.loc[i]['CASH'] - (row.Shares * ((1+impact)*df_prices.loc[i][row.Symbol])) - (commission)           
        else:  # order is SELL
            df_trade.loc[i][row.Symbol] = df_trade.loc[i][row.Symbol] - row.Shares
            df_trade.loc[i]['CASH'] = df_trade.loc[i]['CASH'] + (row.Shares * ((1-impact)*df_prices.loc[i][row.Symbol])) - (commission)
    #print df_trade   

    df_holding = pd.DataFrame(index=df_prices.index, columns = cols)
    df_holding=df_holding.fillna(0)
    df_holding = df_trade.cumsum() 
    df_holding['CASH'] = df_holding['CASH'] + start_val
    df_value = pd.DataFrame(index=df_prices.index, columns = cols)
    for i, row in df_holding.iterrows():
        for sym in syms:
            df_value.loc[i][sym] = row[sym] * df_prices.loc[i][sym]
    
    df_value['CASH'] = df_holding['CASH'] 
    #print df_value

    portvals = df_value.sum(axis=1)    
    #print portvals    
     
    portvals_norm =  portvals/portvals.values[0]
 

    
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_porfolio(port_val = portvals)
    print '\n**********  OPTO LEARNER STRATEGY  **********'
    print "last_day_portval = {}".format(portvals[-1]) #last value or portval
    print "sharpe_ratio = {}".format(sharpe_ratio)
    print "Cumulative return = {}".format(cum_ret)

    
     
#    #    ********************  PLOT   *****************************
#    df_temp = pd.concat([portvals_benchmark_norm, portvals_manual_norm, portvals_norm], keys=['portvals_benchmark','portvals_manual',  'portvals_opto'], axis=1)
#    aa = df_temp.plot(title='Benchmark vs Manual vs Optimization strategy Normalized portvals - IN SAMPLE', color = ['b','black', 'r'],label='benchmark')   
#    aa.set_xlabel("Date")
#    aa.set_ylabel("Normalized portvals ")
#
#    plt.grid()
#    plt.show()
    #    **************************************************************
    return portvals
    print


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


start_date_insample = dt.datetime(2008, 1, 1)
end_date_insample = dt.datetime(2009, 12, 31)
start_date_out_of_sample = dt.datetime(2010, 1, 1)
end_date_out_of_sample = dt.datetime(2011, 12, 31)
port_val = 100000


with open('../data/Lists/sp5002008.txt') as f:
    tickers = f.readlines()

    f = open('univ_test.csv','w+')
    f.write('ticker,cum_ret,sharpe,avg_daily_ret,std_daily_ret\n')

    i = 0
    for ticker in tickers:
        if (i < 1000):
            sym=ticker.strip()
            print sym
            learner = sl.StrategyLearner(verbose=False, impact=0.005)
            learner.addEvidence(symbol=sym, sd=start_date_insample, ed=end_date_insample, sv=port_val)

            df_trades_out = learner.testPolicy(symbol=sym, sd=start_date_out_of_sample, ed=end_date_out_of_sample, sv=port_val)

            if (len(df_trades_out) >0):
                portvals_out_sample_col = marketsim(df_trades_out, port_val, commission=0.00, impact=.005)
                #portvals_out_sample_col = portvals_out_sample[portvals_out_sample.columns[0]]
                cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = assess_porfolio(portvals_out_sample_col)
                f.write("{},{},{},{},{}\n".format(sym, cum_ret, sharpe_ratio, avg_daily_ret, std_daily_ret))
                f.flush()

            print i
        i = i + 1

    f.close()