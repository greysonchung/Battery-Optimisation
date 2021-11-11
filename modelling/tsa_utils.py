import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.seasonal import STL
from filterpy.kalman import KalmanFilter

def compute_adfuller_test(timeseries, maxlag=48):
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    result = adfuller(timeseries, maxlag=maxlag, autolag='AIC')
    output = pd.Series(result[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in result[4].items():
        output['Critical Value (%s)'%key] = value
    print (round(output,4))
    
def plot_tsc(timeseries, lags=48):
    fig, axs = plt.subplots(1, 2, figsize=(16,4))
    plot_acf(timeseries, lags=lags, ax=axs[0])
    axs[0].set_xlabel('Number of Lags')
    axs[0].set_ylabel('Correlation')
    plot_pacf(timeseries, ax=axs[1], lags=lags)
    axs[1].set_xlabel('Number of Lags')
    axs[1].set_ylabel('Correlation')
    plt.show()
    return
    
def plot_seasonal_decompose(timeseries, decompfreq=((24*60)//30), method='LOESS', start=0, end=-1):
    
    # Seasonal decomposition using moving averages
    if method.lower() == 'ma':
        decomposition = seasonal_decompose(timeseries,period=decompfreq) # default with daily seasonality with 30-minute interval
        observed = timeseries
        trend = decomposition.trend
        seasonal =decomposition.seasonal
        resid = decomposition.resid
        fig, axs = plt.subplots(4, 1, figsize=(25,12))
        axs[0].set_title('Observed')
        axs[0].plot(observed[start:end])
        axs[1].set_title('Trend')
        axs[1].plot(trend[start:end])
        axs[2].set_title('Season')
        axs[2].plot(seasonal[start:end])
        axs[3].set_title('Redisual')
        axs[3].plot(resid[start:end])
    
    # Season-Trend decomposition using LOESS.
    elif method.lower() == 'loess':
        fig, axs = plt.subplots(4, 1, figsize=(25,12))
        results = STL(timeseries, period=decompfreq, seasonal=7).fit()
        observed = results.observed
        seasonal = results.seasonal
        trend = results.trend
        resid = results.resid
        axs[0].set_title('Observed')
        axs[0].plot(observed[start:end])
        axs[1].set_title('Trend')
        axs[1].plot(trend[start:end])
        axs[2].set_title('Season')
        axs[2].plot(seasonal[start:end])
        axs[3].set_title('Redisual')
        axs[3].plot(resid[start:end])
    
    plt.tight_layout()
    return plt.show()
    
    
def add_fourier_terms(datetime, year_k, week_k, day_k):
    """
    df: dataframe to add the fourier terms to 
    year_k: the number of Fourier terms the year period should have. Thus the model will be fit on 2*year_k terms (1 term for 
            sine and 1 for cosine)
    week_k: same as year_k but for weekly periods
    day_k:  same as year_k but for daily periods
    """
    
    df = pd.DataFrame({'datetime': datetime}).reset_index(drop=True)
    df.datetime = pd.to_datetime(df.datetime)
    
    for k in range(1, year_k+1):
        # year has a period of 365.25 including the leap year
        df['year_sin'+str(k)] = np.sin(2 *k* np.pi * df.datetime.dt.dayofyear/365.25) 
        df['year_cos'+str(k)] = np.cos(2 *k* np.pi * df.datetime.dt.dayofyear/365.25)

    for k in range(1, week_k+1):
        
        # week has a period of 7
        df['week_sin'+str(k)] = np.sin(2 *k* np.pi * df.datetime.dt.dayofweek/7)
        df['week_cos'+str(k)] = np.cos(2 *k* np.pi * df.datetime.dt.dayofweek/7)


    for k in range(1, day_k+1):
        
        # day has period of 24
        df['hour_sin'+str(k)] = np.sin(2 *k* np.pi * df.datetime.dt.hour/24)
        df['hour_cos'+str(k)] = np.cos(2 *k* np.pi * df.datetime.dt.hour/24) 
    
    return df