import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import datetime

import defunciones_registro
import casos_covid

# cd Downloads\Python\Streamlit
# streamlit run main.py    

# Config
# st.beta_set_page_config(
#     page_title="Covid-19 Chile",
#  	layout="centered",
#  	initial_sidebar_state="expanded",
# )

# Sidebar   
st.sidebar.title('Navegación')
opt = st.sidebar.radio("",
    ("Casos confirmados", "Defunciones Registro Civil", "Defunciones por causa", "Más")
)

if opt == "Defunciones Registro Civil":
    defunciones_registro.main()

if opt == "Casos confirmados":
    casos_covid.main()

if opt == "Defunciones por causa":
    vista_deis.main()

if opt == "Más":
    st.write("En construcción...")
