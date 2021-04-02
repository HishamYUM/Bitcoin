#inportation des bibliothèques nécessaires:
import pandas as pd 
import pandas_datareader.data as pdr
import datetime as dt
import plotly.offline as py # cette méthode (offline) permet de dessiner des graphes offline sur Jupyter Notebook.
import plotly.graph_objs as go
#spécifier l'intervalle de temps au cours duquel on va récupérer BitcoinData.
start = dt.datetime(2020,3,19)
end = dt.datetime(2021,3,18)
#pandas_datareader nous permettra de récupérer les données du site "yahoo" et créer une dataframe.
data_frame = pdr.DataReader('BTC-USD','yahoo',start,end)

py.init_notebook_mode(connected=True)

#Utiliser la méthode 'Candlestick' en lui passant en argument [X abscisse: les dates,Y: les valeurs 'Open' 'High' 'Low' 'Close']
data = [go.Candlestick(x=data_frame.index,
                       open=data_frame.Open,
                       high=data_frame.High,
                       low=data_frame.Low,
                       close=data_frame.Close)]
# définir le Layout du Candlestick, on donne le titre, et on ajoute un Rangeslider (curseur de gamme) comme axe d'abscisse
# + on ajouter the range selector (selecteurs de gamme) , ils générents des boutons pour séléctionner des gammes dans le graphe
layout = go.Layout(title='Bitcoin Candlestick with Range Slider',
                   xaxis={'rangeselector':{'buttons':[{'count':7,
                                                      'label':'last week',
                                                      'step':'day',
                                                      'stepmode':'backward'},
                                                     {'count':1,
                                                      'label':'last month',
                                                      'step':'month',
                                                      'stepmode':'backward'},
                                                    {'count':2,
                                                      'label':'last two months',
                                                      'step':'month',
                                                      'stepmode':'backward'},
                                                    {'count':3,
                                                      'label':'last three months',
                                                      'step':'month',
                                                      'stepmode':'backward'},
                                                      {'count':4,
                                                      'label':'last four months',
                                                      'step':'month',
                                                      'stepmode':'backward'},
                                                      {'count':5,
                                                      'label':'last five months',
                                                      'step':'month',
                                                      'stepmode':'backward'},
                                                    {'count':1,
                                                      'label':'last year',
                                                      'step':'year',
                                                      'stepmode':'backward'},
                                                      ]},'rangeslider':{'visible':True}})

fig = go.Figure(data=data,layout=layout)
py.iplot(fig,filename='bitcoin_candlestick')
