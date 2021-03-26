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


def get_currencies_quotes(start_date: str, end_date: str, id_currency: int):
    start = get_timestamp(start_date)
    end = get_timestamp(end_date)
    url = f'https://web-api.coinmarketcap.com/v2/cryptocurrency/ohlcv/historical?id={id_currency}&convert=USD&time_start={start}&time_end={end}'
    return requests.get(url).json()


for i in coins:
    data = get_currencies_quotes(start_date='2021-03-20 00:00:00', end_date='2021-03-26 00:00:00', id_currency=i)
    data_flat = [quote['quote']['USD'] for quote in data['data']['quotes']]
    df = pd.DataFrame(data_flat)
    print(coins[i])
    df.set_index('timestamp', inplace=True)

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    pd.set_option('display.colheader_justify', 'center')

    print(df, '\n')