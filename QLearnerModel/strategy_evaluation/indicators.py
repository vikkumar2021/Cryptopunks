"""
Student Name: Tommy Habibe (replace with your name)  		  	   		   	 		  		  		    	 		 		   		 		  
GT User ID: thabibe3 (replace with your User ID)  		  	   		   	 		  		  		    	 		 		   		 		  
GT ID: 902970734 (replace with your GT ID)  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  

import matplotlib.pyplot as plt
import pandas as pd

from .util import get_data, plot_data


def author():
    return "thabibe3"


def price_sma_ratio(df, window=14):
    symbol = df.columns[0]
    #print(df.head)
    df['14 day - MA'] = df[symbol].rolling(window).mean()

    df['Price/SMA'] = (df[symbol] / df['14 day - MA']) - 1

    #df['Normalized Price'] = df[symbol] / df[symbol][0]

    #     fig, ax = plt.subplots(dpi=100)
    #     df[['Price/SMA','Normalized Price']].plot(ax=ax)
    #     plt.title('Price/SMA')
    #     plt.ylabel('Ratio')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure3.png')

    #     fig, ax = plt.subplots(dpi=100)
    #     df[[symbol,'14 day - MA']].plot(ax=ax)
    #     plt.title('Price + 14 day MA')
    #     plt.ylabel('Price')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure1.png')

    dfsma = df[['Price/SMA']]
    dfsma[dfsma['Price/SMA'] > 0.20] = 2
    dfsma[dfsma['Price/SMA'] < -0.20] = 1
    dfsma[(dfsma['Price/SMA'] < 0.20) & (dfsma['Price/SMA'] > -0.20)] = 0

    return dfsma

def MACD(df):
    symbol = df.columns[0]
    df['MACD'] = df[[symbol]].ewm(span=12).mean() - df[[symbol]].ewm(span=26).mean()
    df['MACD Signal'] = df[['MACD']].ewm(span=9).mean()
    df['MACD - Signal'] = (df['MACD'] - df['MACD Signal'])
    #df['Normalized Price'] = df[symbol] / df[symbol][0]

    #     fig, ax = plt.subplots(dpi=100)
    #     df[['MACD', 'MACD Signal']].plot(ax=ax)
    #     plt.title('MACD')
    #     plt.ylabel('MACD Value')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure7.png')

    #     fig, ax = plt.subplots(dpi=100)
    #     df[['MACD - Signal','Normalized Price']].plot(ax=ax)
    #     plt.title('MACD - Signal')
    #     plt.ylabel('MACD - Signal')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure8.png')

    dfmacd = df[['MACD - Signal']]
    dfmacd[dfmacd['MACD - Signal'] > 0] = 1
    dfmacd[dfmacd['MACD - Signal'] < 0] = 2

    return dfmacd


def bollinger_bands(df, window=14):
    symbol = df.columns[0]
    df['14 day - MA'] = df[symbol].rolling(window).mean()
    df['StD'] = df[symbol].rolling(window).std()
    df['MA - 2StDev'] = df['14 day - MA'] - 2 * df['StD']
    df['MA + 2StDev'] = df['14 day - MA'] + 2 * df['StD']

    df['BBvalue'] = (df[symbol] - df['14 day - MA']) / (2 * df['StD'])

    #     fig, ax = plt.subplots(dpi=100)
    #     df[[symbol, '14 day - MA', 'MA - 2StDev', 'MA + 2StDev']].plot(ax=ax)
    #     plt.title('Bollinger Bands')
    #     plt.ylabel('Price')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure4.png')

    dfbb = df[['BBvalue']]
    dfbb[dfbb['BBvalue'] <= -1] = 1
    dfbb[dfbb['BBvalue'] >= 1] = 2
    dfbb[(dfbb['BBvalue'] > -1) & (dfbb['BBvalue'] < 1)] = 0
    # display(dfbb)

    return dfbb


def momentum(df, window=14):
    symbol = df.columns[0]
    df['Momentum'] = ((df[symbol][window - 1:] / df[symbol][:-window + 1].values) - 1)
   # df['Normalized Price'] = df[symbol] / df[symbol][0]

    #     fig, ax = plt.subplots(dpi=100)
    #     df[['Momentum','Normalized Price']].plot(ax=ax)
    #     plt.title('Momentum')
    #     plt.ylabel('Momentum Value')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure5.png')

    dfm = df[['Momentum']]
    dfm[dfm['Momentum'] > 0] = 1
    dfm[dfm['Momentum'] <= 0] = 2
    # display(dfm)

    return dfm


def stochastic_oscillator(df, window=14):
    symbol = df.columns[0]
    df['Max'] = df[symbol].rolling(window).max()
    df['Min'] = df[symbol].rolling(window).min()

    df['14-Day SO'] = (df[symbol] - df['Min']) / (df['Max'] - df['Min']) * 100
    df['Smoothed SO'] = df[['14-Day SO']].rolling(window).mean()
    df['Smoothed SO 14 Day MA'] = df[['Smoothed SO']].rolling(window).mean()

    #     fig, ax = plt.subplots(dpi=100)
    #     df[[symbol, 'Smoothed SO', 'Smoothed SO 14 Day MA']].plot(ax=ax)
    #     plt.title('Stochastic Oscillator')
    #     plt.axhline(y=80, color='r', linestyle='--')
    #     plt.axhline(y=20, color='r', linestyle='--')
    #     plt.ylabel('SO Value')
    #     plt.xlabel('Date')
    #     plt.savefig('Figure6.png')

    dfso = df[['Smoothed SO 14 Day MA']]
    dfso[dfso['Smoothed SO 14 Day MA'] <= 20] = 1
    dfso[dfso['Smoothed SO 14 Day MA'] >= 80] = 2
    dfso[(dfso['Smoothed SO 14 Day MA'] > 20) & (dfso['Smoothed SO 14 Day MA'] < 80)] = 0
    # display(dfso)

    return dfso

def test_code():
    symbol = 'JPM'
    start = "1/1/2008"
    end = "12/31/2009"
    spy = get_data([symbol], pd.date_range(start, end))
    spy.drop(columns=['SPY'], inplace=True)
    plot_data(spy)

    bollinger_bands(spy)
    stochastic_oscillator(spy)
    momentum(spy)
    MACD(spy)

if __name__ == "__main__":
    test_code()  		  	   		   	 		  		  		    	 		 		   		 		  
