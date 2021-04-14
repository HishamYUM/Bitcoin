#Ce code fait la conversion des devices (ETH, LTC, BTC, XMR, ETC,BCH, USD (dollar)) en BTC
#Les donnés sont pris du site  https://docs.poloniex.com/#returnticker

from datetime import datetime
import pickle
import pandas as pd
import plotly.offline as py
import plotly.express as px
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
    df = pd.read_json(json_url)
    df.to_pickle(cache_path)          # Pickle (sérialiser) l'objet dans le fichier.
    print('Cached {} at {}'.format(json_url, cache_path))
    return df
base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}' #le site dont on a prit la data
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # up until today
pediod = 86400 # pull daily data (86,400 seconds per day)

def get_crypto_data(poloniex_pair):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df
altcoins = ['BTC_ETH','BTC_LTC','USDC_BTC','BTC_ETC','BTC_STR','BTC_BCH','BTC_XMR']

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
                  'usd': 1/df_usd.close,
                  'etc': df_etc.close,
                  'bch': df_bch.close,
                  'xmr':df_xmr.close
                  })
df=df.fillna(0)
fig = px.line(df)
py.plot(fig)
