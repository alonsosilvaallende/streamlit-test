import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.title("Evolución del total de casos confirmados acumulados por región")
st.markdown("*Advertencia*: El número de casos confirmados no representa exactamente el número de casos/contagios reales. Estos últimos valores no son conocidos por límites de testeo.")

st.markdown("Datos: [Ministerio de Ciencia](https://github.com/MinCiencia/Datos-COVID19)")
@st.cache
def get_data():
	URL = "https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto3/CasosTotalesCumulativo_T.csv"
	df = pd.read_csv(URL)
	return df.set_index("Region")

#try:
#	df = get_data()
#except urllib.error.URLError as e:
#	st.error(
#        """
#        **This demo requires internet access.**
#
#        Connection error: %s
#    """
#		% e.reason
#	)
#	return

df = get_data()

region = st.multiselect(
	"Elegir regiones", list(df.columns), ["Metropolitana", "Valparaíso"]
)
#if not region:
#    st.error("Please select at least one country.")
#    return

df = df[region]
st.write("### Total de casos confirmados acumulados", df.T)
df = df.reset_index()
df = pd.melt(df, id_vars=["Region"], var_name="Región" , value_name="total casos confirmados").rename(columns={"Region": "fecha"})

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="fecha:T",
        y=alt.Y("total casos confirmados", stack=None),
		tooltip = ['fecha', 'total casos confirmados'],
        color="Región:N",
    ).properties(
    	title='Total de casos confirmados acumulados*',
		height=600,
    	width='container'
	)
)

st.altair_chart(chart)#, use_container_width=True)

st.markdown("*El 17 de junio, se añadieron 31.422 casos confirmados debido a revisiones en el sistema de epivigilia y las fuentes de datos ([ver noticia](https://www.biobiochile.cl/noticias/nacional/chile/2020/06/16/minsal-anade-otros-31-412-contagios-covid-19-no-estaban-informados-total-supera-los-215-mil.shtml)).")
