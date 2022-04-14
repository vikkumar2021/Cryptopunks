import pandas as pd
import numpy as np
import json

def categorize_pipeline(df):
    
    with open("config_file.json") as f:

        config = json.load(f)
    
    cols = [('bollinger_band_percentage',3),
            ('stochastic_oscillator_sma',3, config.get("so_ll"), config.get("so_ul")),
            ('rsi',3),
            ("price_to_SMA_ratio", 3, config.get("sma_threshold")),
            ("momentum", 2, config.get("mom_threshold")),
            ('avg_compound_sentiment', 3, config.get("sentiment_threshold")),
            ('macd', 2)]
    
# =============================================================================
#     "sma_threshold" : 0.2,
#     "so_ul" : 80,
#     "so_ll" : 20,
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
    
    print(collist)
    print(onlycols)
    print(combinations)
    
    newdf = df[onlycols]
    for i in collist:
        if len(i) == 4:
            newdf[i[0]][newdf[i[0]]>i[3]] = 2
            newdf[i[0]][newdf[i[0]]<i[2]] = 1
            newdf[i[0]][(newdf[i[0]]<=i[3]) & (newdf[i[0]]>=i[2])] = 0
        else:
            newdf[i[0]][newdf[i[0]]>0] = 2
            newdf[i[0]][newdf[i[0]]<=0] = 1
            
    print(newdf.head)
    
    newdf = newdf[newdf['']]
    
    return newdf, combinations
    
if __name__ == "__main__":
    df = pd.read_csv('pipeline.csv')
    categorize_pipeline(df)
            
    