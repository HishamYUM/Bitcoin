from Historic_Crypto import HistoricalData
import pandas as pd 
from scipy.stats import pearsonr
import matplotlib.pyplot as plt 
import matplotlib.colors as col 
from matplotlib import cm
import numpy as np 

# the price frequency in seconds: 21600 = 6 hour price data, 86400 = daily price data
frequency = 21600
# The beginning of the period for which prices will be retrieved
from_date = '2017-01-01-00-00'
# The currency price pairs for which the data will be retrieved
coinlist = ['ETH-USD', 'BTC-USD']
###########################################import data and insert it to a dataframe###########################################################################
# Query the data
for i in range(len(coinlist)):
    coinname = coinlist[i]
    pricedata = HistoricalData(coinname, frequency, from_date).retrieve_data()
    pricedf = pricedata[['close', 'low', 'high']]
    if i == 0:
        df = pd.DataFrame(pricedf.copy())
    else:
        df = pd.merge(left=df, right=pricedf, how='left', left_index=True, right_index=True)   
    df.rename(columns={"close": "close-" + coinname}, inplace=True)
    df.rename(columns={"low": "low-" + coinname}, inplace=True)
    df.rename(columns={"high": "high-" + coinname}, inplace=True)

#################################this part is about calculating the two indicators and inserting them to the dataframe created previously (df)###############################"
#function calculating and adding indicators: RSI / Correlation to data frame.
def add_indicators(df):
    # Calculate the 30 day Pearson Correlation 
    cor_period = 30 #this corresponds to a monthly correlation period
    columntobeadded = [0] * cor_period
    df = df.fillna(0) 
    for i in range(len(df)-cor_period):
        btc = df['close-BTC-USD'][i:i+cor_period]
        eth = df['close-ETH-USD'][i:i+cor_period]
        corr, _ = pearsonr(btc, eth)
        columntobeadded.append(corr)    
    # insert the colours into our original dataframe    
    df.insert(2, "P_Correlation", columntobeadded, True)

    # Calculate the RSI
    # Moving Averages on high, lows, and std - different periods
    df['MA200_low'] = df['low-BTC-USD'].rolling(window=200).min()
    df['MA14_low'] = df['low-BTC-USD'].rolling(window=14).min()
    df['MA200_high'] = df['high-BTC-USD'].rolling(window=200).max()
    df['MA14_high'] = df['high-BTC-USD'].rolling(window=14).max()

    # Relative Strength Index (RSI)
    df['K-ratio'] = 100*((df['close-BTC-USD'] - df['MA14_low']) / (df['MA14_high'] - df['MA14_low']) )
    df['RSI'] = df['K-ratio'].rolling(window=3).mean() 

    # Replace nas 
    #nareplace = df.at[df.index.max(), 'close-BTC-USD']    
    df.fillna(0, inplace=True)    
    return df 
dfcr = add_indicators(df)
#####################################This part is about converting idicators values to Colors#################################################################################
# function that converts a given set of indicator values to colors
def get_colors(ind, colormap):
    colorlist = []
    norm = col.Normalize(vmin=ind.min(), vmax=ind.max())
    for i in ind:
        colorlist.append(list(colormap(norm(i))))
    return colorlist

# convert the RSI                         
y = np.array(dfcr['RSI'])
colormap = plt.get_cmap('plasma')
dfcr['rsi_colors'] = get_colors(y, colormap)

# convert the Pearson Correlation
y = np.array(dfcr['P_Correlation'])
colormap = plt.get_cmap('plasma')
dfcr['cor_colors'] = get_colors(y, colormap)
###############################################the first indicator plot###########################################################################################
#Creating a Bitcoin Price Chart Colored by RSI
pd.plotting.register_matplotlib_converters()
fig, ax1 = plt.subplots(figsize=(18, 10), sharex=False)
x = dfcr.index
y = dfcr['close-BTC-USD']
z = dfcr['rsi_colors']

# draw points
for i in range(len(dfcr)):
    ax1.plot(x[i], np.array(y[i]), 'o',  color=z[i], alpha = 0.5, markersize=5)
ax1.set_ylabel('BTC-Close in $')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_xlabel('Date')
ax1.text(0.02, 0.95, 'BTC-USD - Colored by RSI',  transform=ax1.transAxes, fontsize=16)


# plot the color bar
pos_neg_clipped = ax2.imshow(list(z), cmap='plasma', vmin=0, vmax=100, interpolation='none')
cb = plt.colorbar(pos_neg_clipped)

####################################################the second indicator plot##########################################################################################
#Creating a Bitcoin Price Chart colored by BTC-ETH Correlation:
pd.plotting.register_matplotlib_converters()
fig, ax1 = plt.subplots(figsize=(18, 10), sharex=False)
x = dfcr.index # datetime index
y = dfcr['close-BTC-USD'] # the price variable
z = dfcr['cor_colors'] # the color coded indicator values

# draw points
for i in range(len(dfcr)):
    ax1.plot(x[i], np.array(y[i]), 'o',  color=z[i], alpha = 0.5, markersize=5)
ax1.set_ylabel('BTC-Close in $')
ax1.tick_params(axis='y', labelcolor='black')
ax1.set_xlabel('Date')
ax1.text(0.02, 0.95, 'BTC-USD - Colored by 50-day ETH-BTC Correlation',  transform=ax1.transAxes, fontsize=16)

# plot the color bar
pos_neg_clipped = ax2.imshow(list(z), cmap='Spectral', vmin=-1, vmax=1, interpolation='none')
cb = plt.colorbar(pos_neg_clipped)
