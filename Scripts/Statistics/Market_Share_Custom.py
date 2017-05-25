import pandas as pd
import numpy as np

def major(x):
    if x in major_exchange:
        return x
    else:
        return "MinorExchanges"

def clean(x):
    if x=="bitfinexUSD":
        return "Bitfinex"
    elif x=="bitstampUSD":
        return "Bitstamp"
    elif x=="btceUSD":
        return "BTCe"
    elif x=="mtgoxUSD":
        return "MtGox"
    elif x=="gdaxUSD":
        return "GDAX"
    elif x=="itbitUSD":
        return "itBit"
    elif x=="localbtcUSD":
        return "LocalBitcoins"
    elif x=="lakeUSD":
        return "Lake"
    elif x=="geminiUSD":
        return "Gemini"
    elif x=="krakenUSD":
        return "Kraken"
    else:
        return x

ms_data = pd.read_csv("C://Honors_Thesis//MonthlyExchangeVolume1.csv")

major_exchange  = ['bitfinexUSD','bitstampUSD','btceUSD','mtgoxUSD','gdaxUSD','itbitUSD','localbtcUSD','lakeUSD','geminiUSD','krakenUSD']
print(len(ms_data.loc[ms_data['Exchange']=='btceUSD']))
ms_data['MajorExchange'] = ms_data['Exchange'].apply(lambda x: major(x))
ms_data['MajorExchange'] = ms_data['MajorExchange'].apply(lambda x: clean(x))
ms_data = ms_data[['Date','MajorExchange','MarketShare']]
ms_data = ms_data.groupby(by=['Date','MajorExchange'],as_index=False)['MarketShare'].sum()
print(ms_data.head())
print(len(ms_data.loc[ms_data['MajorExchange']=='BTCe']))
ms_data.to_csv("MajorExchangeData.csv",index=False)
