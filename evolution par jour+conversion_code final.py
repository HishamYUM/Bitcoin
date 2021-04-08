#################le code est totalement pret , c'est fini pour la conversion + l'evolution par jour
import os
import numpy as np
import pandas as pd
import pickle as pkl
import ccxt
import matplotlib.pyplot as plt
from datetime import datetime
import time

market = ['BTC/USD','LTC/BTC']
def getCCXTData(market):
    '''télécharge et met les données de CCXT en cache'''
    cachePath = '{}.pkl'.format(market).replace('/', '-')
    if os.path.isfile(cachePath):
        dataFile = open(cachePath, 'rb')
        downloadFile = pkl.load(dataFile)
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
usd = pd.read_csv('BTC-USD.csv')
ltc = pd.read_csv('LTC-BTC.csv')
df = pd.DataFrame({'Time': usd.Time ,'USD': usd.close,
                   'LTC': 1/ltc.close})
os.remove('BTC-USD.csv')
os.remove('LTC-BTC.csv')
x = df.Time
y1 =df.USD 
y2 =df.LTC
a = int(input("veuillez saisir le numero de l'operation voulu \n 1/voir l'evolution du bitcoin aujourd'hui\t  2/convertir une devise \n "))
assert a in {1,2} ,"veuillez saisir un 1 ou un 2 !!"
if (a==1):
    plt.plot(x,y1/100, "b-" , label = '$USD/100$') # Setting up legends
    plt.plot(x,y2, "r-" ,label ='$LTC$') # Setting up legends
    plt.xlabel("TIME")
    plt.ylabel("1 BTC vaut :")
    plt.title("$Evolution $ $ BTC $ $ en $ $fonction$ $de$ $LTC$ $et$ $USD$" ,fontsize = 14)
    plt.legend()
    plt.tight_layout()
    print("le tableau presentant l'evolution d'un BTC dans les 6 min prochaines \n" ,df.set_index('Time').head(6))
elif(a==2):
        time =time.strftime('%H:%M:00', time.localtime()) 
        data_extra=df.loc([x for x in df['Time']] == time)
        val_usd=data_extra[2][1]
        val_ltc=data_extra[3][2]
        b=str(input("veuillez saisir la device a convertir   :    USD   LTC   BTC \n"))
        assert b in {'USD','LTC','BTC'},"ERROR"
        c=float(input("veuillez saisir la valeur de la somme a convertir   "))
        d=str(input("veuillez saisir la device voulue   :    USD   LTC   BTC \n"))
        assert d in {'USD','BTC','LTC'},'ERROR'
        if (b=='BTC'):
            if (d=='USD'):
                print (c," ",b,"="," ",c*(val_usd)," ",d )
            elif (d=='LTC'):
                print (c," ",b,"="," ",c*(val_ltc)," ",d )
            else:
                print (c," ",b,"="," ",c," ",d )  
        elif(b=='LTC'):
            if (d=='BTC'):
                print (c," ",b,"="," ",c*(1/(val_ltc))," ",d )
            elif(d=='USD'):
                print (c," ",b,"="," ",c*(val_usd/val_ltc)," ",d )
            else:
                print (c," ",b,"="," ",c," ",d )
        else:
            if (d=='BTC'):
                print (c," ",b,"="," ",c*(1/val_usd)," ",d )
            elif(d=='LTC'):
                print (c," ",b,"="," ",c*(val_ltc/val_usd)," ",d )
            else:
                print (c," ",b,"="," ",c," ",d )      

            
            


                
                
        
        
        





