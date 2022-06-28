# imports needed...
import numpy as np
import pandas as pd

' compute macd '


PRICE_VAL_ARRAY = np.array([1,2,3,4]) # change with real price values over time

# create a DataFrame with price info
df_macd={}
df_macd['mean'] = PRICE_VAL_ARRAY
df_macd = pd.DataFrame(df_macd)

# possible to set our macd params
# if you are interested in this funct  / tool i guess you already now what they are...
# if no check --> https://www.dailyfx.com/education/moving-average-convergence-divergence/macd-settings.html
df_macd.ta.macd(close='mean', fast=25, slow=40, signal=20, append=True)