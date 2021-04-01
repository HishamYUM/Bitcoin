import time
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

cmc = requests.get("https://coinmarketcap.com/currencies/")
soup = BeautifulSoup(cmc.content, 'html.parser')
# print(soup.prettify())
data = soup.find('script', id="__NEXT_DATA__", type="application/json")
coins = {}
coin_data = json.loads(data.contents[0])
listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
for i in listings:
    coins[str(i['id'])] = i['slug']


def get_timestamp(datetime: str):
    return int(time.mktime(time.strptime(datetime, '%Y-%m-%d %H:%M:%S')))


for i in coins:
    data = get_currencies_quotes(start_date='2021-03-20 00:00:00', end_date='2021-03-26 00:00:00', id_currency=i)
    data_flat = [quote['quote']['USD'] for quote in data['data']['quotes']]
    df = pd.DataFrame(data_flat)
    #print(coins[i])
    df.set_index('timestamp', inplace=True)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')
altcoins = ['ETH','LTC','XRP','ETC','STR','DASH','SC','XMR','XEM']

altcoin_data = {}
for altcoin in altcoins:
    coinpair = 'BTC_{}'.format(altcoin)
    crypto_price_df = get_crypto_data(coinpair)
    altcoin_data[altcoin] = crypto_price_df
altcoin_data['ETH'].tail()
df_eth = altcoin_data['ETH']
df_ltc = altcoin_data['LTC']
df_etc = altcoin_data['ETC']
df = pd.DataFrame({'ETH': df_eth.close,
                   'LTC': df_ltc.close,
                  'ETC':df_str.close})
df.head()
df.plot(grid=True, figsize=(15, 10))
