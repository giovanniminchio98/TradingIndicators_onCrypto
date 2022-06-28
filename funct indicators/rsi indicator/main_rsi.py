# imports needed ...
import numpy as np
import pandas as pd

# funct to compute the RSI given the dataFrame
def compute_rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """
    close_delta = df['close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    return rsi

' EXAMPLE OF USE'
# df to compute RSI
CANDELS_INFO = 0 # get actual info from somewhere (personally i use binance api w. function -->)
# example : client.get_historical_klines(coin_pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

# this is to get the mean price...example...
get_close_price_15m =  np.array([float((float(item[4])+float(item[4]))/2) for item in CANDELS_INFO])

# create a Dataframe with the close price info 'close' 
df_rsi = pd.DataFrame({'close':get_close_price_15m}) # normally close price is used
rsi = np.array(compute_rsi(df_rsi)) # this is our rsi