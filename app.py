import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import datetime

st.title("Evolución del total de casos confirmados acumulados por región")
st.markdown("*Advertencia*: El número de casos confirmados no representa exactamente el número de casos/contagios reales. Estos últimos valores no son conocidos por límites de testeo.")
st.markdown("Autor: [Alonso Silva](https://github.com/alonsosilvaallende)")
st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")
@st.cache
def get_data():
	URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv"
	df = pd.read_csv(URL)
	df = df.rename(columns={"Region": "fecha"})
	df["fecha"] = pd.to_datetime(df["fecha"])
	df = df.set_index("fecha")
	df = df.sort_index()
	return df

df = get_data()

region = st.multiselect(
	"Elegir regiones", list(df.columns), ["Metropolitana", "Valparaíso"]
)

start_date = st.date_input('Fecha de inicio', df.index[0])
end_date = st.date_input('Fecha de termino', df.index[-1])
if start_date < end_date:
    st.success('Fecha de inicio: `%s`\n\nFecha de termino: `%s`' % (start_date, end_date))
else:
    st.error('Error: La fecha de término debe ser después de la fecha de inicio.')

df = df[region].loc[start_date:end_date]
st.write("### Total de casos confirmados acumulados", df.T)
df = df.reset_index()
df = pd.melt(df, id_vars=["fecha"], var_name="Región" , value_name="total casos confirmados")#.rename(columns={"Region": "fecha"})

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="fecha:T",
        y=alt.Y("total casos confirmados", stack=None),
		tooltip = ['total casos confirmados'],
        color="Región:N",
    ).properties(
    	title='Total de casos confirmados acumulados*',
		height=600,
    	width=600
	)
)

st.altair_chart(chart)

st.markdown("*El 17 de junio, se añadieron 31.422 casos confirmados debido a revisiones en el sistema de epivigilia y las fuentes de datos ([ver noticia](https://www.biobiochile.cl/noticias/nacional/chile/2020/06/16/minsal-anade-otros-31-412-contagios-covid-19-no-estaban-informados-total-supera-los-215-mil.shtml)).")

st.title("Evolución de nuevos casos confirmados por región")
st.markdown("*Advertencia*: El número de casos confirmados no representa exactamente el número de casos/contagios reales. Estos últimos valores no son conocidos por límites de testeo.")
df = get_data()

df = df.T

df[pd.to_datetime("2020-03-02")] = [0 for i in range(len(df.index))]

df = df.T

df = df.sort_index()

df = df.diff()

#region = st.multiselect(
#	"Elegir regiones", list(df.columns), ["Metropolitana", "Valparaíso"]
#)

#start_date = st.date_input('Fecha de inicio', df.index[0])
#end_date = st.date_input('Fecha de termino', df.index[-1])
#if start_date < end_date:
#    st.success('Fecha de inicio: `%s`\n\nFecha de termino: `%s`' % (start_date, end_date))
#else:
#    st.error('Error: La fecha de término debe ser después de la fecha de inicio.')

df = df[region].loc[start_date:end_date]
st.write("### Nuevos casos confirmados", df.T)
df = df.reset_index()
df = pd.melt(df, id_vars=["fecha"], var_name="Región" , value_name="nuevos casos confirmados")#.rename(columns={"Region": "fecha"})

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="fecha:T",
        y=alt.Y("nuevos casos confirmados", stack=None),
		tooltip = ['nuevos casos confirmados'],
        color="Región:N",
    ).properties(
    	title='Nuevos casos confirmados*',
		height=600,
    	width=600
	)
)

st.altair_chart(chart)

st.markdown("*El 17 de junio, se añadieron 31.422 casos confirmados debido a revisiones en el sistema de epivigilia y las fuentes de datos ([ver noticia](https://www.biobiochile.cl/noticias/nacional/chile/2020/06/16/minsal-anade-otros-31-412-contagios-covid-19-no-estaban-informados-total-supera-los-215-mil.shtml)).")


