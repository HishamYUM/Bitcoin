import pickle
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.offline as py


def get_json_data(json_url, cache_path):
    '''Téléchargez et mettez en cache les données JSON, retournez-les sous forme de dataframe.'''
    '''JSON est un raccourci pour la notation d'objets JavaScript. Il s'agit d'un format de texte 
            souvent utilisé pour échanger des données sur le Web.'''
    df = pd.read_json(json_url)#Convertissez une chaîne JSON en un Pandas DataFrame.
    df.to_pickle(cache_path)# Pickle (sérialiser) l'objet dans le fichier.
    print('Cached {} at {}'.format(json_url, cache_path))# c est la phrase qui s'affiche avant la visualisation du graphe
    return df#df c est la data frame


base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'#le site dont on a prit la data
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d')  # get data from the start of 2015
end_date = datetime.now()  # jusqu'à aujourd'hui
pediod = 86400  # extraire des données quotidiennes (86 400 secondes par jour)


def get_crypto_data(poloniex_pair):
    '''Récupérer les données de crypto-monnaie de poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    #il remplace la premiére accolade par poloniex_pair, le deuxieme par le nombre de seconde depuis start_date,la troisieme par le nombre de seconde depuis end_date,et a la fin par 86400
    #La fonction timestamp () renvoie l'heure exprimée en nombre de secondes
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')#Définir l'index pour qu'il devienne la colonne "date"
    return data_df


def allcoins():
    altcoins = ['BTC_ETH', 'BTC_LTC', 'USDC_BTC', 'BTC_ETC', 'BTC_STR', 'BTC_BCH', 'BTC_XMR']

    altcoin_data = {} #création d'un dictionnaire vide 
    for altcoin in altcoins:
        coinpair = altcoin
        crypto_price_df = get_crypto_data(coinpair) #Récupérer les données de crypto-monnaie de la liste altcoins du site poloniex
        altcoin_data[altcoin] = crypto_price_df #ajouter les donnés de chaque crypto-monnaie au dictionnaire altcoin_data
    #on affecte a df_eth la valeur du dictionnaire correspondant à la clé 'BTC_ETH' et on fait la méme chose por les autres crypto-monnaie 
    df_eth = altcoin_data['BTC_ETH'] 
    df_ltc = altcoin_data['BTC_LTC']
    df_usd = altcoin_data['USDC_BTC']
    df_etc = altcoin_data['BTC_ETC']
    df_bch = altcoin_data['BTC_BCH']
    df_xmr = altcoin_data['BTC_XMR']
    #Nous fusionnons les cours de clôture  ETH, LTC,USD,ETC,BCH et XMR dans une Dataframe 
    df = pd.DataFrame({'ETH': df_eth.close,
                       'LTC': df_ltc.close,
                       'USD': 1 / df_usd.close,
                       'ETC': df_etc.close,
                       'BCH': df_bch.close,
                       'XMR': df_xmr.close})
    #plot des altcoins
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
    py.plot(fig, filename='allcoins.html', auto_open=True, config=config)
    div = pio.to_html(fig, include_plotlyjs=False)
    return div
allcoins()
