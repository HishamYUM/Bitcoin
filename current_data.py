import os
import numpy as np
import pandas as pd
import pickle
import ccxt
import matplotlib.pyplot as plt
from datetime import datetime
def getCCXTData(market):
    '''télécharge et met les données de CCXT en cache'''
    cachePath = '{}.pkl'.format(market).replace('/', '-')
    if os.path.isfile(cachePath):
        dataFile = open(cachePath, 'rb')
        downloadFile = pickle.load(dataFile)
        print('{} est chargé du cache'.format(market))
    else:
        dataFile = open(cachePath, 'wb')
        print('Charge de {} de CCXT'.format(market))
        exchange = ccxt.bittrex()
        downloadFile = exchange.fetch_ohlcv(market, timeframe = '1m') # 1 minute
        dataFrame = pd.DataFrame(data=downloadFile, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        dataFrame.to_pickle(cachePath)
        print('{} en cache dans {}'.format(market, cachePath))
    return downloadFile
# def loadData():
#     '''télécharge les données de Bittrex'''
#     getCCXTData('BTC/USD')



# loadData()
altcoinsData = {}
def loadData():
    altcoins = ['BTC/USD','LTC/BTC']
    for market in altcoins:
        altcoinsData[market] = getCCXTData(market)
        altcoinsData[market]['timestamp'] = [datetime.fromtimestamp(x/1000) for x in altcoinsData[market]['timestamp']]
        print(altcoinsData[market].head())


loadData()
