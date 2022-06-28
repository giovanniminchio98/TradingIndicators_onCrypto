# imports needed...
import numpy as np
import pandas as pd
from datetime import datetime

# to plot candels
import mplfinance as mpf



# function to tell if candels sequence is for support or resistence
# using naive candels pattern for supp and res ...
def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]
  return support
def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]
  return resistance

def isFarFromLevel(l):
    global s
    global levels
    return np.sum([abs(l-x) < s  for x in levels]) == 0

# get the candels info ..
CANDELS_INFO = 0 # get actual info from somewhere (personally i use binance api w. function -->)
# example : 
# CANDELS_INFO = client.get_historical_klines(coin_pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

# get single prices info to create "pandas candel"
get_open_price =  np.array([float((float(item[1])+float(item[1]))/2) for item in CANDELS_INFO])
get_high_price =  np.array([float((float(item[2])+float(item[2]))/2) for item in CANDELS_INFO])
get_low_price =  np.array([float((float(item[3])+float(item[3]))/2) for item in CANDELS_INFO])
get_close_price =  np.array([float((float(item[4])+float(item[4]))/2) for item in CANDELS_INFO])


candels = {}
candels['Open'] = get_open_price
candels['High'] = get_high_price
candels['Low'] = get_low_price
candels['Close'] = get_close_price

date_time =  np.array([datetime.fromtimestamp(item[0]/1000.0) for item in CANDELS_INFO])
candels['Date'] = date_time

# average candel dimension, used to check is subsequent support / resistence are mergable or not (jsut consider them a single one or not)
s =  0#np.mean(candels['High'] - candels['Low'])*0.4


candels = pd.DataFrame(candels)
candels.set_index('Date', inplace=True)

# computations to detect support and resistence
levels=[]
hline_level = []
markers=[]
for i in range(2,candels.shape[0]-2):
    if isSupport(candels,i):
        l = candels['Low'][i]
        if isFarFromLevel(l):
            levels.append((i,l))
            a = [(candels.index[i], l), (candels.index[i+2], l)]
            hline_level.append(a)

    elif isResistance(candels,i):
        l = candels['High'][i]
        if isFarFromLevel(l):
            levels.append((i,l))
            a = [(candels.index[i], l), (candels.index[i+2], l)]
            hline_level.append(a)
    
mpf.plot(
    candels.iloc[:],
    mav=(7,25),
    type='candle', 
    volume=False, 
    figratio=(24,12), 
    style='yahoo', 
    title='test',
    block=False,
    alines=dict(alines=hline_level, linestyle='-.')
)

breakpoint()