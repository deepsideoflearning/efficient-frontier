from PIL import Image
import streamlit as st
from constants import *
import datetime
import requests
import json
import pandas as pd
import seaborn as sn
import matplotlib.pyplot as plt


if __name__=='__main__':
    st.header('Efficient Frontier')

    st.sidebar.title('Navigation')

    ct = datetime.datetime.now()
    st.sidebar.write("Current time:", ct)

    coin_table=pd.DataFrame(columns=['coin'])

    coin_table.loc[0]='BTC'
    coin_table.loc[1]='ETH'
    coin_table.loc[2]='BNB'
    for i in range(7):
        coin_table.loc[i+3]=''
        
    for i in range(10):
        coin_table.loc[i]=st.sidebar.text_input("Coin "+str(i)+":", coin_table.loc[i])

    # Get Data

    endpoint = 'https://min-api.cryptocompare.com/data/histoday'
    hist_all=pd.DataFrame()

    for i, coin in coin_table.iterrows():
        print(coin['coin'])
        res = requests.get(endpoint + '?fsym='+coin['coin']+'&tsym=USD&limit=2000')
        hist = pd.DataFrame(json.loads(res.content)['Data'])
        hist = hist.set_index('time')
        hist.index = pd.to_datetime(hist.index, unit='s')
        hist_all[coin['coin']] = hist[['close']]
   
    hist_all['date']=hist.index

    hist_year = hist_all[pd.DatetimeIndex(hist_all['date']).month*pd.DatetimeIndex(hist_all['date']).day==1]
    hist_year.drop(['date'],axis=1,inplace=True)
    
    st.header('Annual activity')
    st.write(hist_year.sort_values(by=['time'], ascending=False))
    
    hist_month = hist_all[pd.DatetimeIndex(hist_all['date']).day==1]
    hist_month.drop(['date'],axis=1,inplace=True)

    st.header('monthly activity')
    st.write(hist_month.sort_values(by=['time'], ascending=False))
    
    corr_matrix =hist_year.corr()
    st.write(corr_matrix)

    fig, ax = plt.subplots()
    sn.heatmap(corr_matrix, annot=True)
    st.write(fig)
