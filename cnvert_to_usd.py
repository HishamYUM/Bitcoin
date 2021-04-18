from datetime import datetime #permet la manipulation des dates
import pickle
import pandas as pd
import plotly.offline as py
import plotly.express as px
def get_json_data(json_url, cache_path):
    '''Téléchargez et mettez en cache les données JSON, retournez-les sous forme de dataframe.'''
    '''JSON est un raccourci pour la notation d'objets JavaScript. Il s'agit d'un format de texte 
            souvent utilisé pour échanger des données sur le Web.'''
    df = pd.read_json(json_url)#Convertissez une chaîne JSON en un Pandas DataFrame.
    df.to_pickle(cache_path)# Pickle (sérialiser) l'objet dans le fichier.
    print('Cached {} at {}'.format(json_url, cache_path))# c est la phrase qui s'affiche avant la visualisation du graphe
    return df#df c est la data frame
base_polo_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'#le site dont on a prit la data
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # jusqu'à aujourd'hui
pediod = 86400 # extraire des données quotidiennes (86 400 secondes par jour)

def get_crypto_data(poloniex_pair):
    '''Récupérer les données de crypto-monnaie de poloniex'''
    json_url = base_polo_url.format(poloniex_pair, start_date.timestamp(), end_date.timestamp(), pediod)
    #il remplace la premiére accolade par poloniex_pair, le deuxieme par le nombre de seconde depuis start_date,la troisieme par le nombre de seconde depuis end_date,et a la fin par 86400
    #La fonction timestamp () renvoie l'heure exprimée en nombre de secondes
    data_df = get_json_data(json_url, poloniex_pair)
    data_df = data_df.set_index('date')#Définir l'index pour qu'il devienne la colonne "date"
    return data_df
altcoins = ['USDC_ETH','USDC_LTC','USDC_BTC','USDC_ETC','USDC_STR','USDC_BCH','USDC_XMR']

altcoin_data = {}#création d'un dictionnaire vide
for altcoin in altcoins:
    coinpair = altcoin
    crypto_price_df = get_crypto_data(coinpair)#Récupérer les données de crypto-monnaie de la liste altcoins du site poloniex
    altcoin_data[altcoin] = crypto_price_df#ajouter les donnés de chaque crypto-monnaie au dictionnaire altcoin_data
#on affecte a df_eth la valeur du dictionnaire correspondant à la clé 'USDC_ETH' et on fait la méme chose por les autres crypto-monnaie 
df_eth = altcoin_data['USDC_ETH']
df_ltc = altcoin_data['USDC_LTC']
df_btc = altcoin_data['USDC_BTC']
df_etc = altcoin_data['USDC_ETC']
df_bch = altcoin_data['USDC_BCH']
df_xmr = altcoin_data['USDC_XMR']
#Nous fusionnons les cours de clôture  ETH, LTC,USD,ETC,BCH et XMR dans une Dataframe 
df = pd.DataFrame({'ETH': df_eth.close,
                  'LTC': df_ltc.close,
                  'btc': df_btc.close,
                  'etc': df_etc.close,
                  'bch': df_bch.close,
                  'xmr':df_xmr.close
                  })
#plot des altcoins
df=df.fillna(0)
fig = px.line(df)
py.plot(fig)
