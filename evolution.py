import os
import numpy as np
import pandas as pd
import pickle as pkl
import ccxt
import csv
import matplotlib.pyplot as plt 
from datetime import datetime
usd = pd.read_csv('BTC-USD.csv')
ltc = pd.read_csv('LTC-BTC.csv')
##BTC-USD donne 1 bitcoin combien en USD et LTC-BTC donne 1LTC en bitcoin , on fait l'oppose pour avoir 1BTC en litcoin
df = pd.DataFrame({'Time': usd.timestamp ,'USD': usd.close,
                   'LTC': 1/ltc.close})
x = df.Time
y1 =df.USD 
y2 =df.LTC
plt.plot(x,y1, "b-" , label = '$USD$') # Setting up legends
plt.plot(x,y2, "r-" ,label ='$LTC$') # Setting up legends
plt.xlabel("TIME")
plt.ylabel("1 BTC vaut:")
plt.legend()
plt.tight_layout()
df
