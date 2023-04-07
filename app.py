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

    coin_choice = st.sidebar.text_input("Coin:", "BTC")

    # Get Data

    endpoint = 'https://min-api.cryptocompare.com/data/histoday'
    res = requests.get(endpoint + '?fsym='+coin_choice+'&tsym=USD&limit=3000')
    hist = pd.DataFrame(json.loads(res.content)['Data'])

    hist = hist.set_index('time')
    hist.index = pd.to_datetime(hist.index, unit='s')
    hist['date']=hist.index

    hist.drop(["conversionType", "conversionSymbol"], axis = 'columns', inplace = True)
    
    hist_year = hist[pd.DatetimeIndex(hist['date']).month*pd.DatetimeIndex(hist['date']).day==1]
    
    st.header(coin_choice +' daily activity')
    st.write(hist_year.sort_values(by=['time'], ascending=False))
    
