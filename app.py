import numpy as np
import pandas as pd
import altair as alt
import streamlit as st

st.title("This is the title")
st.markdown("This is some random **text**")

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
	"Choose countries", list(df.columns), ["Metropolitana", "Valparaíso"]
)
#if not region:
#    st.error("Please select at least one country.")
#    return

df = df[region]
st.write("### Total casos confirmados acumulados", df.T)
df = df.reset_index()
df = pd.melt(df, id_vars=["Region"], var_name="Región" , value_name="Casos confirmados").rename(columns={"Region": "fecha"})

chart = (
    alt.Chart(df)
    .mark_line(opacity=0.3)
    .encode(
        x="fecha:T",
        y=alt.Y("Casos confirmados", stack=None),
        color="Región:N",
    )
)

st.altair_chart(chart)#, use_container_width=True)
