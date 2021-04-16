import json
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import render_template

cmc = requests.get("https://coinmarketcap.com/currencies/")
soup = BeautifulSoup(cmc.content, 'html.parser')

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


mycoins = {'bitcoin': '1', 'ethereum': '1027', 'cardano': '2010', 'xrp': '52', 'litecoin': '2', 'tron': '1958',
           'vechain': '3077', 'electroneum': '2137', 'syscoin': '541'}


def show_history(currency):
    p = datetime.today()
    end_date = p.strftime("%Y-%m-%d %H:%M:%S")
    data = get_currencies_quotes(start_date='2021-03-02 00:00:00', end_date=end_date,
                                 id_currency=int(mycoins[currency]))
    data_flat = [quote['quote']['USD'] for quote in data['data']['quotes']]
    df = pd.DataFrame(data_flat)
    df = df.iloc[::-1]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['timestamp'] = df['timestamp'].map(lambda x: x.strftime('%Y - %m - %d'))
    df.set_index('timestamp', inplace=True)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.colheader_justify', 'center')
    return render_template('view_history.html', tables=[df.to_html(classes='df')], c=currency.capitalize(),
                           titles=[currency])
