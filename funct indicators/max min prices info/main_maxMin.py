# imports needed...
from scipy.signal import argrelextrema
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def get_max_min(prices, smoothing, window_range):
    smooth_prices = prices['close'].rolling(window=smoothing).mean().dropna()
    local_max = argrelextrema(smooth_prices.values, np.greater)[0]
    local_min = argrelextrema(smooth_prices.values, np.less)[0]
    price_local_max_dt = []
    for i in local_max:
        if (i>window_range) and (i<len(prices)-window_range):
            price_local_max_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmax())
    price_local_min_dt = []
    for i in local_min:
        if (i>window_range) and (i<len(prices)-window_range):
            price_local_min_dt.append(prices.iloc[i-window_range:i+window_range]['close'].idxmin())  
    maxima = pd.DataFrame(prices.loc[price_local_max_dt])
    minima = pd.DataFrame(prices.loc[price_local_min_dt])
    max_min = pd.concat([maxima, minima]).sort_index()
    # max_min.index.name = 'date'
    # max_min = max_min.reset_index()
    # max_min = max_min[~max_min.date.duplicated()]
    # p = prices.reset_index()   
    # max_min['day_num'] = p[p['timestamp'].isin(max_min.date)].index.values
    # max_min = max_min.set_index('day_num')['close']
    
    return maxima, minima

CANDELS_INFO = 0 # get actual info from somewhere (personally i use binance api w. function -->)
# example : 
# CANDELS_INFO = client.get_historical_klines(coin_pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

# this is to get the mean price...example...
get_mean_price =  np.array([float((float(item[1])+float(item[4]))/2) for item in CANDELS_INFO])

df={}
df['close'] = get_mean_price
df['id'] = np.arange(len(CANDELS_INFO))
dff = pd.DataFrame(df)


smoothing = 5
window = 5
maxima, minima = get_max_min(dff, smoothing, window)

plt.plot(get_mean_price)
plt.scatter(maxima.id, maxima.close, color='red', alpha=.5)
plt.scatter(minima.id, minima.close, color='green', alpha=.5)
plt.show()