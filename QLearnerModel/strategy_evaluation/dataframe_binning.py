import datetime as dt
import json

import numpy as np
import pandas as pd


def categorize_pipeline(df, config):
    
    cols = [('bollinger_band_percentage',3,0,1),
            ('stochastic_oscillator_sma',3, float(config.get("so_ll")), float(config.get("so_ul"))),
            ('rsi',3),
            ("price_to_SMA_ratio", 3, float(config.get("sma_threshold"))),
            ("momentum", 3, float(config.get("mom_threshold"))),
            ('avg_compound_sentiment', 3, -1*float(config.get("sentiment_threshold")), float(config.get("sentiment_threshold"))),
            ('macd', 3)]
    
# =============================================================================
#     "sma_threshold" : 0.2,
#     "so_ul" : 80,
#     "so_ll" : 20
#     "mom_threshold" : 0.2,
#     "sentiment_threshold": 0.3
# =============================================================================
    
    dfcols = df.columns.tolist()
    
    collist = []
    
    for i in cols:
        if i[0] in dfcols:
            collist.append(i)
    
    onlycols = ["TradeDate","Adj_Close"]
    combinations = 1
    for i in collist:
        combinations = combinations*i[1]
        onlycols.append(i[0])
    
    #print(collist)
    #print(onlycols)
    #print(combinations)
    
    newdf = df[onlycols]
    for i in collist:
        if len(i) == 4:
            newdf[i[0]][newdf[i[0]]>i[3]] = 2
            newdf[i[0]][newdf[i[0]]<i[2]] = 1
            newdf[i[0]][(newdf[i[0]]<=i[3]) & (newdf[i[0]]>=i[2])] = 0
        else:
            newdf[i[0]][newdf[i[0]]>0] = 2
            newdf[i[0]][newdf[i[0]]<=0] = 1
    
    
    newdf['TradeDate'] = pd.to_datetime(newdf['TradeDate'])
    
    
    newdf = newdf.replace([None], np.nan, regex=True)
    newdf = newdf.replace(r'^\s*$', np.nan, regex=True)
    newdf = newdf.dropna()
    
    #newdf['Adj_Close'] = newdf['Adj_Close'].round()
    
    for i in onlycols[1:]:
        newdf[i] = newdf[i].astype('int32')
    
    newdf = newdf.reset_index(drop=True)
    
    return newdf, combinations
    
if __name__ == "__main__":
    df = pd.read_csv('pipeline.csv')
    categorize_pipeline(df)
            
    