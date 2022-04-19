"""MLT: Utility code.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
Copyright 2017, Georgia Tech Research Corporation  		  	   		   	 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332-0415  		  	   		   	 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		   	 		  		  		    	 		 		   		 		  
"""

import os

import pandas as pd

CWD = os.path.dirname(os.path.abspath(__file__))


def symbol_to_path(symbol, base_dir=None):
    """Return CSV file path given ticker symbol."""
    if base_dir is None:
        base_dir = os.environ.get("MARKET_DATA_DIR", "../data/")
    return os.path.join(CWD, "{}.csv".format(str(symbol)))


def get_data(symbol, dates, addSPY=False, colname="Adj_Close"):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    df_temp = pd.read_csv(
        symbol_to_path(symbol[0]),
        index_col="Date",
        parse_dates=True,
        usecols=["Date", colname],
        na_values=["nan"],
    )

    df_temp = df_temp.rename(columns={"Date": "TradeDate"})
    df_temp = df_temp.rename(columns={"Adj Close": "Adj_Close"})

    df = df.join(df_temp)

    return df


def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    import matplotlib.pyplot as plt

    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()


def get_orders_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("ORDERS_DATA_DIR", "orders/"), basefilename)
    )


def get_learner_data_file(basefilename):
    return open(
        os.path.join(os.environ.get("LEARNER_DATA_DIR", "Data/"), basefilename),
        "r",
    )


def get_robot_world_file(basefilename):
    return open(
        os.path.join(os.environ.get("ROBOT_WORLDS_DIR", "testworlds/"), basefilename)
    )
