import streamlit as st
import numpy as np
import pandas as pd
import json
import datetime
from datetime import datetime

import itertools

import openpyxl

import plotly.express as px

st.set_page_config(layout='wide')


st.title("Digital infrastructure in EMEA")

st.header("Deals")

bigdf = pd.DataFrame()

# for i in range(1,16):
#     with open('transactions_'+str(i)+'.json',encoding='utf-8') as data_file:
#         data = json.load(data_file)
#         data = data['transactions']
#         df = pd.json_normalize(data)
#         bigdf = pd.concat([bigdf,df])

# bigdf.to_excel('digital_infra.xlsx')
# bigdf

bigdf = pd.read_excel('digital_infra.xlsx')

countries = bigdf['dominantCountry'].unique().tolist()
countries.sort()

bigdf['lenders']=bigdf['lenders'].apply(eval)

bigdf['transactionStatusDate'] = pd.to_datetime(bigdf['transactionStatusDate'],errors='coerce')
bigdf['Year']= bigdf['transactionStatusDate'].apply(lambda x: x.year)


for col in bigdf.columns:
    try:
        bigdf[col]=bigdf[col].apply(eval)
    except:
        pass

lenderslist = []
for lender in bigdf['lenders']:
    lenderslist.append(lender)

uniquelenderslist = list(itertools.chain.from_iterable(lenderslist))
uniquelenderslist = list(set(uniquelenderslist))
uniquelenderslist.sort()


sectorslist = []
for sector in bigdf['dominantSubsector']:
    sectorslist.append(sector)

# uniquesectorlist = list(itertools.chain.from_iterable(sectorslist))
uniquesectorlist = list(set(sectorslist))
uniquesectorlist.sort()

def lenderindeal(lendergroup,lenderlist):
    for lender in lenderlist:
        if lender in lendergroup:
            ingroup = True
        else:
            ingroup=False
    return ingroup


def sectorindeal(sectorgroup,sectorlist):
    for sector in sectorlist:
        if sector in sectorgroup:
            ingroup = True
        else:
            ingroup=False
    return ingroup


with st.form('Filters'):
    bankfunding = st.checkbox('Bank funded deals only',value=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        bankfilter = st.multiselect('Lender group contains',uniquelenderslist)
    with col2:
        countryfilter = st.multiselect('Select deal countries',countries)
    with col3:
        sectorfilter = st.multiselect('Select sectors',uniquesectorlist)

    period = st.slider('Select time period',min_value=2021,max_value=2023,value=(2021,2023),step=1)
    st.form_submit_button('Submit')

if bankfunding:
    bigdf = bigdf[bigdf['bankFundingTotalUSD']>0]
if len(countryfilter)>0:
    bigdf = bigdf[bigdf['dominantCountry'].isin(countryfilter)]
if len(bankfilter)>0:
    bigdf = bigdf[bigdf['lenders'].apply(lambda x: lenderindeal(x,bankfilter)==True)]
if len(sectorfilter)>0:
    bigdf = bigdf[bigdf['dominantSubsector'].apply(lambda x: sectorindeal(x,sectorfilter)==True)]
bigdf = bigdf[(bigdf['Year']>=period[0])&(bigdf['Year']<=period[1])]

bigdf

@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

csv = convert_df(bigdf)

st.download_button(label='Download data as CSV',data=csv,file_name='export.csv',mime='text/csv')

### sizevalueEUR: compare deal size of NLB vs deal size of Market (distribution)
### distribution by dominantSubsector (by deal amount)
### lendersFundingValues
### summary.bankdebtsizeEUR -> do a treemap by deal type and lenders
### 360 deals in Telecommunications since 2001
