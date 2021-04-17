#ce code nous permet de decider quand vendre et acheter du bitcoin a partir de la valeur du close par rapport au min et max des 28 dernier jour 
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
        data = bitcoin.copy()#créer une copie du dataframe bitcoin
        data['Buy'] = np.zeros(len(data))#on crée une colonne buy et on l'initialise avec des zeros
        data['Sell'] = np.zeros(len(data))#on crée une colonne sell et on l'initialise avec des zeros
        '''cela nous donne la ligne au milieu'''
        #on crée un colonne RollingMax
        #rolling(window=28).max() permet de calculer le max sur les 28 dernier jour du data['Close']
        data['RollingMax'] = data['Close'].shift(1).rolling(window=28).max()
        #on crée un colonne RollingMin
        #rolling(window=28).min() permet de calculer le min sur les 28 dernier jour du data['Close']
        #on décale le signal d'un jour par shift(1) pour que je puisse vendre ou acheter le bitcoin
        data['RollingMin'] = data['Close'].shift(1).rolling(window=28).min()
        #on utilise le boolean indexing lorsque la valeur du close est supérieure au max des 28 dernier jour c'est un signe qu'il faut acheter
        #on écrit 1 a l'intérieure de la colonne Buy si la max est inférieure a la valeur close
        data.loc[data['RollingMax'] < data['Close'], 'Buy'] = 1
        #lorsque la valeur du close est inférieure au min des 28 dernier jour c'est un signe qu'il faut vendre nos action
        #on écrit -1 a l'intérieure de la colonne Sell si la min est supérieure a la valeur close
        data.loc[data['RollingMin'] > data['Close'], 'Sell'] = -1
        '''cette partie permet de générer le graphe avec plotly'''
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
    py.plot(fig, filename='buy&sell.html', config=config, auto_open=True)

    div = pio.to_html(fig, include_plotlyjs=False)

    return div
buy_sell()
