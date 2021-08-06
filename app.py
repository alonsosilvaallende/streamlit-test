import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
df = px.data.gapminder()
fig = px.scatter(df, x="gdpPercap", y="lifeExp", labels={"gdpPercap": "PIB per cápita ajustado por inflación en escala logarítmica (dólares)", "lifeExp":"Esperanza de vida (años)", "continent": "continente", "pop":"población", "year": "año"}, title="Esperanza de vida vs PIB per cápita", animation_frame="year", animation_group="country",
           size="pop", color="continent", hover_name="country",
           log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])
st.plotly_chart(fig)
