import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import datetime

@st.cache
def get_data():
	URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv"
	df = pd.read_csv(URL)
	df = df.rename(columns={"Region": "fecha"})
	df["fecha"] = pd.to_datetime(df["fecha"])
	df = df.set_index("fecha")
	df = df.sort_index()
	return df

@st.cache
def get_population():
    URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto7/PCR.csv"
    df = pd.read_csv(URL)
    df = df[["Region", "Poblacion"]]
    df = df.set_index("Region")
    return df

def my_altair_plot(df, value_name, title):
	df = df.reset_index()
	df = pd.melt(df, id_vars=["fecha"], var_name="Región" , value_name=value_name)
	
	chart = (
	    alt.Chart(df)
	    .mark_line()
	    .encode(
	        x="fecha:T",
	        y=alt.Y(value_name, stack=None),
			tooltip = [value_name],
	        color="Región:N",
	    ).properties(
	    	title=title,
			height=600,
	    	width=600
		)
	)
	return chart
	
df = get_data()

region = st.multiselect(
	"Elegir regiones", list(df.columns), ["Atacama", "Ñuble", "Magallanes"]
)

opciones = ["Total de casos confirmados acumulados", "Total de casos confirmados acumulados por 100.000 habitantes", "Nuevos casos confirmados", "Nuevos casos confirmados por 100.000 habitantes"]
plot = st.selectbox(
	"Elegir gráfico", opciones
)

start_date = df.index[0]
end_date = df.index[-1]

if plot == "Nuevos casos confirmados":
	# Agregar el 2 de marzo para hacer el diff
	df = df.T
	df[pd.to_datetime("2020-03-02")] = [0 for i in range(len(df.index))]
	df = df.T
	df = df.sort_index()
	df = df.diff()
elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
	pop = get_population()
	df = df.T
	pop = pop.reset_index().append({"Region": "Total", "Poblacion": pop["Poblacion"].sum()}, ignore_index=True)
	pop = pop.set_index("Region")
	df["Población"] = pop
	df = df.apply(lambda x: 100000*x[:-1]/x[-1], axis=1)
	df = df.T
elif plot == "Nuevos casos confirmados por 100.000 habitantes":
	# Agregar el 2 de marzo para hacer el diff
	df = df.T
	df[pd.to_datetime("2020-03-02")] = [0 for i in range(len(df.index))]
	df = df.T
	df = df.sort_index()
	df = df.diff()
	pop = get_population()
	df = df.T
	pop = pop.reset_index().append({"Region": "Total", "Poblacion": pop["Poblacion"].sum()}, ignore_index=True)
	pop = pop.set_index("Region")
	df["Población"] = pop
	df = df.apply(lambda x: 100000*x[:-1]/x[-1], axis=1)
	df = df.T

df = df[region].loc[start_date:end_date]

if plot == "Total de casos confirmados acumulados":
	st.title("Evolución del total de casos confirmados acumulados por región")
elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
	st.title("Evolución del total de casos confirmados acumulados por 100.000 habitantes/tasa de incidencia acumulada por región")
elif plot == "Nuevos casos confirmados":
	st.title("Evolución de nuevos casos confirmados por región")
else:
	st.title("Evolución de nuevos casos confirmados por 100.000 habitantes/tasa de incidencia por región")
	
show_df = st.checkbox("Mostrar Tabla")
if show_df:
	st.write(df)

pm = st.checkbox("Promedio móvil 7 días", True)
if pm:
	df = df.rolling(window=7).mean()
df = df.sort_index(ascending=False)

if plot == "Total de casos confirmados acumulados":
	title = "Total de casos confirmados acumulados*"
elif plot == "Total de casos confirmados acumulados por 100.000 habitantes":
	title = "Total de casos confirmados acumulados por 100.000 habitantes*"
elif plot == "Nuevos casos confirmados":
	title = "Nuevos casos confirmados*"
else:
	title = "Nuevos casos confirmados por 100.000 habitantes*"
chart = my_altair_plot(df, "casos confirmados", title)
st.altair_chart(chart)

start_date = st.date_input('Fecha de inicio', df.index[-1])
end_date = st.date_input('Fecha de término', df.index[0])

if start_date > end_date:
    st.error('Error: La fecha de término debe ser después de la fecha de inicio.')

st.markdown("Autor: [Alonso Silva](https://github.com/alonsosilvaallende)")
st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")

st.markdown("*El 17 de junio, se añadieron 31.422 casos confirmados debido a revisiones en el sistema de epivigilia y las fuentes de datos ([ver noticia](https://www.biobiochile.cl/noticias/nacional/chile/2020/06/16/minsal-anade-otros-31-412-contagios-covid-19-no-estaban-informados-total-supera-los-215-mil.shtml)).")

st.markdown("*Advertencia*: El número de casos confirmados no representa exactamente el número de casos/contagios reales. Estos últimos valores no son conocidos por límites de testeo. Además, los casos confirmados por 100.000 habitantes, dan mayores valores a regiones con pocos habitantes, por lo que pueden introducir sesgos en los datos.")
