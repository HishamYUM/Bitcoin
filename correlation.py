#Mesurer la corrélation des cours de cloture
'''Nous calculons la corrélation de Pearson entre les cours de clôture de BCH, ETH, LTC, BTC, XMR, ETC et USD. La corrélation de Pearson est une mesure de la corrélation linéaire
entre deux variables X et Y. Elle a une valeur comprise entre +1 et −1, où 1 est la corrélation linéaire positive totale, 0 est aucune corrélation linéaire et −1 est la linéaire négative totale corrélation. 
La matrice de corrélation est symétrique, nous ne montrons donc que la moitié inférieure.
Sifr Data met à jour quotidiennement les corrélations Pearson pour de nombreuses crypto-monnaies.
df utilise dans ce code est pris du code plot_of_altcoins.py'''


from datetime import datetime
import pickle
import pandas as pd
import plotly.offline as py
import plotly.express as px
def get_json_data(json_url, cache_path):
    '''Download and cache JSON data, return as a dataframe.'''
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
altcoins = ['USDC_ETH','USDC_LTC','USDC_BTC','USDC_ETC','USDC_STR','USDC_BCH','USDC_XMR']

altcoin_data = {}
for altcoin in altcoins:
    coinpair = altcoin
    crypto_price_df = get_crypto_data(coinpair)
    altcoin_data[altcoin] = crypto_price_df
df_eth = altcoin_data['USDC_ETH']
df_ltc = altcoin_data['USDC_LTC']
df_btc = altcoin_data['USDC_BTC']
df_etc = altcoin_data['USDC_ETC']
df_bch = altcoin_data['USDC_BCH']
df_xmr = altcoin_data['USDC_XMR']
df = pd.DataFrame({'ETH': df_eth.close,
                  'LTC': df_ltc.close,
                  'BTC': df_btc.close,
                  'ETC': df_etc.close,
                  'BCH': df_bch.close,
                  'XMR':df_xmr.close
                  })

df=df.fillna(0)

import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
# Calculer la matrice de corrélation
corr = df.corr()
# Générer un masque pour le triangle supérieur
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True
# Configurer la figure matplotlib
f, ax = plt.subplots(figsize=(10, 10))
# Dessinez la carte thermique avec le masque et le rapport hauteur / largeur correct
fig = px.imshow(corr, labels=dict(x="Currency", y="Currency", color="Correlation Value"))
# fig.show()
fig.update_layout(paper_bgcolor="#89acac", plot_bgcolor="#111111", title={
    'text': "calculate the correlation value of some cryptocurrencies",
    'y': 0.989,
    'x': 0.4,
    'xanchor': 'center',
    'yanchor': 'top'},
                  title_font_size=25,
                  title_font_color='#fff',
                  autosize=True,
                  margin=dict(l=0, r=0, t=28.5, b=20),
                  width=800,
                  xaxis_showgrid=False, yaxis_showgrid=False,
                  height=500)
# config = dict({'scrollZoom': True})
py.plot(fig, filename='correlation.html', auto_open=True)
# corr.head()
