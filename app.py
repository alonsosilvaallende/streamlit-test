import streamlit as st
import numpy as np
import pandas as pd
import wbdata
import plotly.express as px

indicators = {'SI.POV.GINI':'Gini Index', 
              'NY.GDP.PCAP.PP.KD':'GDP per capita (constant 2010 US$)',
              'SP.POP.TOTL':'Population'}

data = wbdata.get_dataframe(indicators=indicators)

data = data.reset_index()

df_region = pd.DataFrame()
df_region["Country"]=[row['name'] for row in wbdata.get_country("")]
df_region["Region"]=[row['region']['value'] for row in wbdata.get_country("")]
df_region = df_region.set_index("Country")

df = pd.DataFrame()
for country in data["country"].unique():
    if data[data["country"]==country]['Gini Index'].notna().sum() != 0 and data[data["country"]==country]['GDP per capita (constant 2010 US$)'].notna().sum() != 0:
        df_aux = data[data["country"]==country].fillna(method="bfill").dropna()
        df_aux["Region"]=[df_region.loc[country].values[0] for i in range(len(df_aux))]
        df_aux=df_aux.sort_values(by="date")
        df = pd.concat([df, df_aux], ignore_index=True)

df["date"] = df["date"].astype('int64')
df = df[df["date"]>=1996]
fig = px.scatter(df,
                x='GDP per capita (constant 2010 US$)',
                y='Gini Index',
                animation_frame="date",
                animation_group="country",
                size="Population",
                color="Region",
                hover_name="country",
                log_x=True,
                size_max=55
                )
st.plotly_chart(fig)
