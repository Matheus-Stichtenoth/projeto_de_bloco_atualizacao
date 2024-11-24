import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import fetch_bcb_data, load_local_backup, calculate_indebtedness
from services.page_curiosidades_llm import page_curiosidades_llm
from services.page_map import page_map
from services.page_home import page_home

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
    elif choice == 'Home':
        page_home()

if __name__ == '__main__':
    dashboard()