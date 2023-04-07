from PIL import Image
import streamlit as st
from constants import *
import datetime
import requests
import json
import pandas as pd


if __name__=='__main__':
    st.header('Efficient Frontier')

    st.sidebar.title('Navigation')

    ct = datetime.datetime.now()
    st.sidebar.write("Current time:", ct)

    coin_choice1 = st.sidebar.text_input("Coin 1:", "BTC")
    coin_choice2 = st.sidebar.text_input("Coin 2:", "ETH")
    coin_choice3 = st.sidebar.text_input("Coin 3:", "BNB")

    # Get Data

    endpoint = 'https://min-api.cryptocompare.com/data/histoday'
    res = requests.get(endpoint + '?fsym='+coin_choice1+'&tsym=USD&limit=2000')
    hist1 = pd.DataFrame(json.loads(res.content)['Data'])
    res = requests.get(endpoint + '?fsym='+coin_choice2+'&tsym=USD&limit=2000')
    hist2 = pd.DataFrame(json.loads(res.content)['Data'])
    res = requests.get(endpoint + '?fsym='+coin_choice3+'&tsym=USD&limit=2000')
    hist3 = pd.DataFrame(json.loads(res.content)['Data'])

    hist1 = hist1.set_index('time')
    hist1.index = pd.to_datetime(hist1.index, unit='s')
    hist1['date']=hist1.index
    hist2 = hist2.set_index('time')
    hist2.index = pd.to_datetime(hist2.index, unit='s')
    hist2['date']=hist2.index
    hist3 = hist3.set_index('time')
    hist3.index = pd.to_datetime(hist3.index, unit='s')
    hist3['date']=hist3.index

    hist = hist1[['close','date']]
    hist['close2'] = hist2[['close']]
    hist['close3'] = hist3[['close']]

    hist_year = hist[pd.DatetimeIndex(hist['date']).month*pd.DatetimeIndex(hist['date']).day==1]
    hist_year.drop(['date'],axis=1,inplace=True)
    
    st.header('Annual activity')
    st.write(hist_year.sort_values(by=['time'], ascending=False))
    
    hist_month = hist[pd.DatetimeIndex(hist['date']).day==1]
    hist_month.drop(['date'],axis=1,inplace=True)

    st.header('monthly activity')
    st.write(hist_month.sort_values(by=['time'], ascending=False))
    
    corr_matrix =hist_year.corr()
    st.write(corr_matrix)
    
