########## mzl anzid l'option dyal l'utilisateur 
import os
import numpy as np
import pandas as pd
import pickle as pkl
import ccxt
import matplotlib.pyplot as plt
from datetime import datetime
#########3partie lwla data
market = ['BTC/USD','LTC/BTC']
def getCCXTData(market):
    '''télécharge et met les données de CCXT en cache'''
    cachePath = '{}.pkl'.format(market).replace('/', '-')
    if os.path.isfile(cachePath):
        dataFile = open(cachePath, 'rb')
        downloadFile = pickle.load(dataFile)
    else:
        dataFile = open(cachePath, 'wb')
        exchange = ccxt.bittrex()
        downloadFile = exchange.fetch_ohlcv(market, timeframe = '1m') # 1 minute
        dataFrame = pd.DataFrame(data=downloadFile, columns=['Time', 'open', 'high', 'low', 'close', 'volume'])
        dataFrame['Time'] = [datetime.time(datetime.fromtimestamp(int(time)/1000)) for time in dataFrame['Time']]
        dataFrame.to_pickle(cachePath)
        return (downloadFile)    
def Loaddata():
    for x in market:
        data = getCCXTData(x)
Loaddata()
##########conversion + supression fichier pkl
with open("LTC-BTC.pkl", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'LTC-BTC.csv')
os.remove('LTC-BTC.pkl')
with open("BTC-USD.pkl", "rb") as f:
    object = pkl.load(f)
    
df = pd.DataFrame(object)
df.to_csv(r'BTC-USD.csv')
os.remove('BTC-USD.pkl')
######tableau+ graphe
usd = pd.read_csv('BTC-USD.csv')
ltc = pd.read_csv('LTC-BTC.csv')
df = pd.DataFrame({'Time': usd.Time ,'USD': usd.close,
                   'LTC': 1/ltc.close})
os.remove('BTC-USD.csv')
os.remove('LTC-BTC.csv')
x = df.Time
y1 =df.USD 
y2 =df.LTC
plt.plot(x,y1/100, "b-" , label = '$USD/100$') # Setting up legends
plt.plot(x,y2, "r-" ,label ='$LTC$') # Setting up legends
plt.xlabel("TIME")
plt.ylabel("1 BTC vaut :")
plt.title("$Evolution $ $ BTC $ $ en $ $fonction$ $de$ $LTC$ $et$ $USD$" ,fontsize = 14)
plt.legend()
plt.tight_layout()
df.set_index(['Time','USD','LTC'])
