import os
import pickle as pkl
from datetime import datetime

import ccxt
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as py

market = ['BTC/USD', 'LTC/BTC']


def getCCXTData(market):
    cachePath = '{}.pkl'.format(market).replace('/', '-')
    if os.path.isfile(cachePath):
        dataFile = open(cachePath, 'rb')
        downloadFile = pkl.load(dataFile)
    else:
        dataFile = open(cachePath, 'wb')
        exchange = ccxt.bittrex()
        downloadFile = exchange.fetch_ohlcv(market, timeframe='1m')
        dataFrame = pd.DataFrame(data=downloadFile, columns=['Time', 'open', 'high', 'low', 'close', 'volume'])
        dataFrame['Time'] = [datetime.time(datetime.fromtimestamp(int(time) / 1000)) for time in dataFrame['Time']]
        dataFrame.to_pickle(cachePath)
        return downloadFile


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
df = pd.DataFrame({'Time': usd.Time, 'USD': usd.close,
                   'LTC': 1 / ltc.close})
os.remove('BTC-USD.csv')
os.remove('LTC-BTC.csv')


def plot_evolution_garph():
    layout = go.Layout(title={
        'text': "Bitcoin evolution (in US Dollar): Last 24h",
        'y': 0.988,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig = go.Figure(layout=layout)
    x = df.Time
    y1 = df.USD

    fig.add_trace(go.Scatter(x=x, y=y1, name='Bitcoin'))

    fig.update_layout(
        autosize=True,
        margin=dict(l=20, r=50, t=22, b=20),
        width=900,
        xaxis_showgrid=False, yaxis_showgrid=False,
        height=500, paper_bgcolor="#58aa4d", plot_bgcolor="#111444")
    config = dict({'scrollZoom': True})

    py.plot(fig, filename='templates/evolution_per_day.html', auto_open=False, config=config)

    evo = pio.to_html(fig, include_plotlyjs=False)

    return evo


# plot_evolution_garph()

def convert_currencies(from_currency, to_currency, amount):
    import time

    time = time.strftime('%H:%M:00', time.localtime())
    data_extra = df.loc([x for x in df['Time']] == time)
    val_usd = data_extra[2][1]
    val_ltc = data_extra[3][2]
    if from_currency == 'BTC':
        if to_currency == 'USD':
            result = amount * val_usd
        elif to_currency == 'LTC':
            result = amount * val_ltc
        else:
            result = amount
    elif from_currency == 'LTC':
        if to_currency == 'BTC':
            result = amount * (1 / val_ltc)
        elif to_currency == 'USD':
            result = amount * (val_usd / val_ltc)
        else:
            result = amount
    else:
        if to_currency == 'BTC':
            result = amount * (1 / val_usd)
        elif to_currency == 'LTC':
            result = amount * (val_ltc / val_usd)
        else:
            result = amount
    return str(result)
