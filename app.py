import streamlit as st
import numpy as np
import pandas as pd
import wbdata
import plotly.express as px

@st.cache
def get_data():
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
	df = pd.concat([df[df["country"]=="Chile"],df[df["country"]!="Chile"]], ignore_index=True)
	return df

df = get_data()
texts = st.checkbox("Mostrar nombres de los países")
if texts:
	text="country"
else:
	text=None
fig = px.scatter(df,
                x='GDP per capita (constant 2010 US$)',
                y='Gini Index',
				text=text,
                animation_frame="date",
                animation_group="country",
                size="Population",
                color="Region",
                hover_name="country",
                log_x=True,
                size_max=60,
				labels={"Gini Index":"Índice de Gini",
 "GDP per capita (constant 2010 US$)":"PIB per cápita (dólares ajustados por inflación a valor 2010) (escala log)"},
				title="Índice de Gini vs PIB per cápita"
                )
st.plotly_chart(fig)
st.write("Elaboración propia en base a datos del Banco Mundial")
st.write("Autor: Alonso Silva")
# with st.expander("See explanation"):
# 	st.write("""
# 			La siguiente es la explicación
# 	""")
