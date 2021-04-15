import time

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import plotly.offline as py



def buy_sell():
    fig = go.Figure()

    t = round(time.time())

    pairs = ['BTC-USD']
    for i in pairs:
        bitcoin = pd.read_csv(
            'https://query1.finance.yahoo.com/v7/finance/download/{}?period1=1586613499&period2={}&interval=1d&events=history&includeAdjustedClose=true'.format(
                i, t), index_col='Date', parse_dates=True)
        data = bitcoin.copy()
        data['Buy'] = np.zeros(len(data))
        data['Sell'] = np.zeros(len(data))
        data['RollingMax'] = data['Close'].shift(1).rolling(window=28).max()
        data['RollingMin'] = data['Close'].shift(1).rolling(window=28).min()
        data.loc[data['RollingMax'] < data['Close'], 'Buy'] = 1
        data.loc[data['RollingMin'] > data['Close'], 'Sell'] = -1
        start = '2020'
        end = '2021'
    fig.add_trace(go.Scatter(x=data.index, y=data['Buy'][start:end], name='Buy'))

    fig.add_trace(go.Scatter(x=data.index, y=data['Sell'][start:end], name='Sell'))
    fig.update_layout(
        autosize=True,
        width=1000,
        margin=dict(l=20, r=5, t=28, b=20),
        title={
        'text': "Buy/Sell",
        'y':0.988,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        height=500, paper_bgcolor="#58aa4d", plot_bgcolor="#111444")


    config = dict({'scrollZoom': True})
    py.plot(fig, filename='templates/buy&sell.html', config=config, auto_open=False)

    div = pio.to_html(fig, include_plotlyjs=False)

    return div
# buy_sell()
