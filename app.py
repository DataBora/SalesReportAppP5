#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


# In[2]:


st.set_page_config(page_title='Sales Report')
st.header('SALES REPORT', anchor=None)
st.subheader('Solution by Borivoj Grujičić')


# In[3]:


image = Image.open('images/bizanaliza.JPG')
st.image(image,
        use_column_width=False)


# In[4]:


df = pd.read_excel('Sales.xlsx')


# In[5]:


YEAR = df['YEAR'].unique().tolist()
MONTH = df['MONTH'].unique().tolist()
WH = df['WH'].unique().tolist()
COLOUR = df['COLOUR'].unique().tolist()
DAYNAME = df['DAYNAME'].unique().tolist()


# In[6]:


# STREAMLIT SELECTION

year_selection = st.slider('YEAR:',
                        min_value= min(YEAR),
                        max_value= max(YEAR),
                        value=(min(YEAR),max(YEAR)))

month_selection = st.slider('MONTH:',
                        min_value= min(MONTH),
                        max_value= max(MONTH),
                        value=(min(MONTH),max(MONTH)))

WH_selection = st.multiselect('WH:',
                                    WH,
                                    default=WH)

colour_selection = st.multiselect('COLOUR:',
                                    COLOUR,
                                    default=COLOUR)

dayname_selection = st.multiselect('DAYNAME:',
                                    DAYNAME,
                                    default=DAYNAME)


# In[7]:


# FILTER DATAFRAME BASED ON SELECTION

mask = (df['YEAR'].between(*year_selection)) & (df['MONTH'].between(*month_selection)) & (df['WH'].isin(WH_selection)) & (df['COLOUR'].isin(colour_selection)) & (df['DAYNAME'].isin(dayname_selection))
number_of_result = df[mask].shape[0]
st.markdown(f'*Available Results: {number_of_result}*')


# In[8]:


# GROUP DATAFRAME AFTER SELECTION

df_grouped = df[mask].groupby('YEAR').REVENUE.sum()
df_grouped = df_grouped.reset_index()


# In[9]:


# GROUP1 DATAFRAME AFTER SELECTION

df_grouped1 = df[mask].groupby('WH').REVENUE.sum()
df_grouped1 = df_grouped1.reset_index()


# In[10]:


# GROUP2 DATAFRAME AFTER SELECTION

df_grouped2 = df[mask].groupby('DAYNAME').REVENUE.sum()
df_grouped2 = df_grouped2.reset_index()


# In[11]:


# PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                   title= 'Sales chart',
                   x='YEAR',
                   y='REVENUE',
                   text='REVENUE',
                   color_discrete_sequence = ['#F63366']*len(df_grouped),
                   template= 'plotly_white')
st.plotly_chart(bar_chart)


# In[12]:


# PLOT PIE CHART
pie_chart = px.pie(df,
                title='Total Sales by Colour',
                values='REVENUE',
                names='COLOUR')

st.plotly_chart(pie_chart)

