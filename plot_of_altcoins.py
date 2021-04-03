#Visualisez les cours de clôture absolus
from datetime import datetime
import pickle
import pandas as pd
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
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
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # up until today
pediod = 86400 # pull daily data (86,400 seconds per day)

def get_crypto_data(poloniex_pair):
    '''Retrieve cryptocurrency data from poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')
    return data_df
altcoins = ['BTC_ETH','BTC_LTC','USDC_BTC']

altcoin_data = {}
for altcoin in altcoins:
    coinpair = altcoin
    crypto_price_df = get_crypto_data(coinpair)
    altcoin_data[altcoin] = crypto_price_df
#altcoin_data['ETH'].tail()
df_eth = altcoin_data['BTC_ETH']
df_ltc = altcoin_data['BTC_LTC']
df_btc = altcoin_data['USDC_BTC']
df = pd.DataFrame({'ETH': df_eth.close,
                  'LTC': df_ltc.close,
                  'BTC': df_btc.close})
df.head()
df.plot(grid=True, figsize=(15, 10))
