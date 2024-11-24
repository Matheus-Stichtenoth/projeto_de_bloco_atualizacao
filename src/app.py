import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import fetch_bcb_data, load_local_backup, calculate_indebtedness
from services.page_curiosidades_llm import page_curiosidades_llm
from services.page_map import page_map

menu_lateral = [
    'Home',
    'Curiosidades',
    'Mapa de Inadimplência'
]

st.image('data\Titulo.png')

def dashboard() -> None:
    choice = st.sidebar.selectbox('Páginas', menu_lateral)
    if choice == 'Curiosidades':
        page_curiosidades_llm()
    elif choice == 'Mapa de Inadimplência':
        page_map()
    else:
        st.image('data/capa_riskmap.png',width = 10000)

if __name__ == '__main__':
    dashboard()