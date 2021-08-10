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
	df = pd.concat([df[df["country"]=="Austria"],df[df["country"]!="Austria"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="Algeria"],df[df["country"]!="Algeria"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="Botswana"],df[df["country"]!="Botswana"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="Australia"],df[df["country"]!="Australia"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="India"],df[df["country"]!="India"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="United States"],df[df["country"]!="United States"]], ignore_index=True)
	df = pd.concat([df[df["country"]=="Chile"],df[df["country"]!="Chile"]], ignore_index=True)
	return df

df = get_data()
option = st.multiselect('Elige regiones de interes', df["Region"].unique().tolist(), df["Region"].unique().tolist())
selected = st.multiselect('Elige países de interés', ['Todos']+df["country"].unique().tolist())
df_aux = pd.DataFrame()
for i,region in enumerate(option):
	df_aux = pd.concat([df_aux, df[df["Region"]==option[i]]], ignore_index=True)
if len(df_aux) == 0:
	st.error("Por favor, ingrese una región")
else:
	df_aux["selected country"] = ['' for i in range(len(df_aux))]
	if len(selected) != 0:
		for i, cntry in enumerate(selected):
			if selected[i] == 'Todos':
				selected = df["country"].unique().tolist()
	for selection in selected:
		df_aux.loc[df_aux.index[df_aux["country"]==f"{selection}"].tolist(), "selected country"] = f"{selection}"
	fig = px.scatter(df_aux,
	                x='GDP per capita (constant 2010 US$)',
	                y='Gini Index',
					text='selected country',
	                animation_frame="date",
	                animation_group="country",
	                size="Population",
	                color="Region",
	                hover_name="country",
	                log_x=True,
	                size_max=60,
					range_x=[df_aux['GDP per capita (constant 2010 US$)'].min(),df_aux['GDP per capita (constant 2010 US$)'].max()],
					range_y=[df_aux['Gini Index'].min(), df_aux['Gini Index'].max()],
					labels={"Gini Index":"Índice de Gini",
	 "GDP per capita (constant 2010 US$)":"PIB per cápita (dólares ajustados por inflación a valor 2010) (escala log)"},
					title="Índice de Gini vs PIB per cápita"
	                )
	st.plotly_chart(fig)
	st.write("Elaboración propia en base a datos del Banco Mundial")
	st.write("Autor: Alonso Silva")
