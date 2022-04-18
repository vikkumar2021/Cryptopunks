""""""  		  	   		   	 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
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

import math
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data


def author():
    return "thabibe3"


def compute_portvals(orders_df, start_val=100000, commission=0, impact=0):
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Computes the portfolio values.
    :param orders_file: Path of the order file or the file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		   	 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		   	 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		   	 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading
    day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		  	   		   	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		   	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input
    # uTODO: Your code here
    # In the template, instead of computing the value of the portfolio, we just  		  	   		   	 		  		  		    	 		 		   		 		  
    # read in the value of IBM over 6 months
    
    start = orders_df.loc[0]['TradeDate']
    end = orders_df.loc[len(orders_df) - 1]['TradeDate']

    tickers = orders_df['Symbol'].unique()

    port_vals = get_data([tickers[0]], pd.date_range(start, end), addSPY=False)
    port_vals['Cash'] = 1

    trades_df = port_vals.copy()
    commission_df = port_vals.copy()
    impact_df = port_vals.copy()

    for col in trades_df.columns:
        trades_df[col] = float(0)
        commission_df[col] = float(0)
        impact_df[col] = float(0)
        
    symbol = 'Adj_Close'
    for i in range(len(orders_df)):
        d = orders_df.loc[i]['TradeDate']
        amount = orders_df.loc[i]['Shares']
        if orders_df.loc[i]['Order'] == 'BUY':
            sign = 1
        elif orders_df.loc[i]['Order'] == 'SELL':
            sign = -1
        
        trades_df.loc[d][symbol] = trades_df.loc[d][symbol] + sign * amount
        impact_df.loc[d][symbol] = impact_df.loc[d][symbol] + amount * impact
        commission_df.loc[d][symbol] = commission_df.loc[d][symbol] + commission

    cost_df = port_vals * trades_df + port_vals * impact_df + commission_df
    #print(cost_df.head)
    
    trades_df['Cash'] = -1 * cost_df.sum(axis=1)
    #print(trades_df.head)

    holdings_df = port_vals.copy()
    for col in trades_df.columns:
        holdings_df[col] = 0

    dates = holdings_df.index
    holdings_df = holdings_df.reset_index(drop=True).copy()
    trades_df2 = trades_df.reset_index(drop=True).copy()

    for i in range(len(holdings_df)):
        if i == 0:
            holdings_df.loc[i] = trades_df2.loc[i]
            holdings_df.loc[i]['Cash'] = start_val + trades_df2.loc[i]['Cash']
        else:
            holdings_df.loc[i] = holdings_df.loc[i - 1] + trades_df2.loc[i]

    holdings_df['TradeDate'] = dates
    holdings_df = holdings_df.set_index('TradeDate')
    #print(holdings_df)

    vals = port_vals * holdings_df
    #print(vals.head)
    vals_sum = pd.DataFrame(vals.sum(axis=1), columns=['Sum'])
    #print(vals_sum.head)
    return vals_sum

def stats(df):
    adj_cum_pos_returns = ((df / df.iloc[0]) - 1)
    total_adjusted_cum_return = adj_cum_pos_returns.iloc[-1].sum()

    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns.iloc[0, :] = 0
    daily_returns = daily_returns[1:]
    adj_daily_returns = daily_returns
    total_adj_daily_returns = adj_daily_returns.sum(axis=1)

    total_adjusted_avg_daily_ret = total_adj_daily_returns.mean()
    total_adjusted_std_daily_ret = total_adj_daily_returns.std()

    sharp = math.sqrt(252) * total_adjusted_avg_daily_ret / total_adjusted_std_daily_ret

    return total_adjusted_cum_return, total_adjusted_avg_daily_ret, total_adjusted_std_daily_ret, sharp

def test_code():
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    Helper function to test code  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		  	   		   	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		  	   		   	 		  		  		    	 		 		   		 		  
    # Define input parameters  		  	   		   	 		  		  		    	 		 		   		 		  

    of = "./orders/orders2.csv"
    sv = 1000000

    orders_df = pd.read_csv(of, na_values=['nan'])
    orders_df = orders_df.sort_values(by=['TradeDate'])
    # Process orders  		  	   		   	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file=orders_df, start_val=sv)

    # Get portfolio stats  		  	   		   	 		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.
    start = orders_df.loc[0]['TradeDate']
    end = orders_df.loc[len(orders_df) - 1]['TradeDate']

    spy = get_data(['$SPX'], pd.date_range(start, end))
    spy.drop(columns=['SPY'], inplace=True)

    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = stats(portvals)
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY =  stats(spy)

    # Compare portfolio against $SPX  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Date Range: {start} to {end}")
    print()  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print()  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print()  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		   	 		  		  		    	 		 		   		 		  
    print()  		  	   		   	 		  		  		    	 		 		   		 		  
    print(f"Final Portfolio Value: {portvals.loc[end]['Sum']}")

    plot_data(portvals, title='Fund', xlabel='Day', ylabel='Price')
    print(author())

if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    test_code()  		  	   		   	 		  		  		    	 		 		   		 		  
