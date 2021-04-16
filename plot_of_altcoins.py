import pickle
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.offline as py


def get_json_data(json_url, cache_path):
    try:
        f = open(cache_path, 'rb')
        df = pickle.load(f)
        print('Loaded {} from cache'.format(json_url))
    except (OSError, IOError) as e:
        print('Downloading {}'.format(json_url))
        df = pd.read_json(json_url)
        df.to_pickle(cache_path)
        print('Cached {} at {}'.format(json_url, cache_path))
    return df


base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')  # get data from the start of 2015
end_date = datetime.now()  # up until today
pediod = 86400  # pull daily data (86,400 seconds per day)


def get_crypto_data(poloniex_pair):
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df


def allcoins():
    altcoins = ['BTC_ETH', 'BTC_LTC', 'USDC_BTC', 'BTC_ETC', 'BTC_STR', 'BTC_BCH', 'BTC_XMR']

    altcoin_data = {}
    for altcoin in altcoins:
        coinpair = altcoin
        crypto_price_df = get_crypto_data(coinpair)
        altcoin_data[altcoin] = crypto_price_df
    df_eth = altcoin_data['BTC_ETH']
    df_ltc = altcoin_data['BTC_LTC']
    df_usd = altcoin_data['USDC_BTC']
    df_etc = altcoin_data['BTC_ETC']
    df_bch = altcoin_data['BTC_BCH']
    df_xmr = altcoin_data['BTC_XMR']
    df = pd.DataFrame({'ETH': df_eth.close,
                       'LTC': df_ltc.close,
                       'USD': 1 / df_usd.close,
                       'ETC': df_etc.close,
                       'BCH': df_bch.close,
                       'XMR': df_xmr.close
                       })
    df = df.fillna(0)
    fig = px.line(df)
    fig.update_layout(paper_bgcolor="#1188fc", plot_bgcolor="#111111", title={
        'text': "Evolution of some cryptocurrencies in terms of Bitcoin since 2015",
        'y': 0.989,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
                      title_font_size=25,
                      title_font_color='#fff',
                      autosize=True,
                      margin=dict(l=20, r=50, t=28.5, b=20),
                      width=1300,
                      xaxis_showgrid=False, yaxis_showgrid=False,
                      height=600)
    config = dict({'scrollZoom': True})
    py.plot(fig, filename='templates/allcoins.html', auto_open=False, config=config)
    div = pio.to_html(fig, include_plotlyjs=False)
    return div
