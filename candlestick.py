import datetime as dt

import pandas_datareader.data as pdr
import plotly.graph_objs as go
import plotly.io as pio
import plotly.offline as py

pio.renderers.default = 'browser'


def plot_graph():
    start = dt.datetime(2019, 1, 1)
    end = dt.datetime.today()
    data_frame = pdr.DataReader('BTC-USD', 'yahoo', start, end)
    data = [go.Candlestick(x=data_frame.index,
                           open=data_frame.Open,
                           high=data_frame.High,
                           low=data_frame.Low,
                           close=data_frame.Close)]
    layout = go.Layout(xaxis={'rangeselector': {'buttons': [{'count': 7,
                                                             'label': 'last week',
                                                             'step': 'day',
                                                             'stepmode': 'backward'},
                                                            {'count': 1,
                                                             'label': 'last month',
                                                             'step': 'month',
                                                             'stepmode': 'backward'},
                                                            {'count': 2,
                                                             'label': 'last two months',
                                                             'step': 'month',
                                                             'stepmode': 'backward'},
                                                            {'count': 3,
                                                             'label': 'last three months',
                                                             'step': 'month',
                                                             'stepmode': 'backward'},
                                                            {'count': 4,
                                                             'label': 'last four months',
                                                             'step': 'month',
                                                             'stepmode': 'backward'},
                                                            {'count': 5,
                                                             'label': 'last five months',
                                                             'step': 'month',
                                                             'stepmode': 'backward'},
                                                            {'count': 1,
                                                             'label': 'last year',
                                                             'step': 'year',
                                                             'stepmode': 'backward'},
                                                            ]}, 'rangeslider': {'visible': True}})

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(paper_bgcolor="#4aaaca", plot_bgcolor="#111111", autosize=True,
                      margin=dict(l=20, r=50, t=22, b=20),
                      width=1200,
                      xaxis_showgrid=False, yaxis_showgrid=False,
                      height=700)
    config = dict({'scrollZoom': True})
    py.plot(fig, filename='templates/bitcoin_candlestick.html', auto_open=False, config=config)
    div = pio.to_html(fig, include_plotlyjs=False)
    return div
