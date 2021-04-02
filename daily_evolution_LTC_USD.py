######kay3ti had lcode 1BTC x7al en LTC et USD f un jour et par seconde , le resultat c un graphe +tableau 
import os
import numpy as np
import pandas as pd
import pickle as pkl
import ccxt
import csv
import matplotlib.pyplot as plt 
from datetime import datetime
#ana lpkl 5al9li 3ou9da f7yati kaymrdni dooonc convertit les fichiers en csv (voir dak lcode d conversion)
usd = pd.read_csv('BTC-USD.csv')
ltc = pd.read_csv('LTC-BTC.csv')
##BTC-USD donne 1 bitcoin combien en USD et LTC-BTC donne 1LTC en bitcoin , on fait l'oppose pour avoir 1BTC en litcoin
df = pd.DataFrame({'Time': usd.timestamp ,'USD': usd.close,
                   'LTC': 1/ltc.close})
x = df.Time
y1 =df.USD 
y2 =df.LTC
plt.plot(x,y1/100, "b-" , label = '$USD/100$') # Setting up legends # s4rt dik USD bax yban lgraphe 7sn i mean les changements b7it houma s4ar bzf
plt.plot(x,y2, "r-" ,label ='$LTC$') # Setting up legends
plt.xlabel("TIME")
plt.ylabel("1 BTC vaut:")
plt.title("$Evolution $ $ BTC $ $ en $ $fonction$ $de$ $LTC$ $et$ $USD$" ,fontsize = 14)
plt.legend()
plt.tight_layout()
df
