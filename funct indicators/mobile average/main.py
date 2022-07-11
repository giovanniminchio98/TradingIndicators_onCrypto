import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if __name__=='__main__':
    CLOSE_PRICE = ['get price via api / file']
    df={}
    df['close'] = CLOSE_PRICE
    dff = pd.DataFrame(df)
    media7 = np.array(dff.rolling(window=7).mean()).reshape((len(dff.rolling(window=7).mean())))

    plt.plot(media7)