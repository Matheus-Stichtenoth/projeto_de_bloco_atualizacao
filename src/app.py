import sys
import os

# Adiciona o diretório do projeto ao caminho do Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from utils import fetch_bcb_data, load_local_backup, calculate_indebtedness
from services.page_curiosidades_llm import page_curiosidades_llm
from services.page_dash import page_dash
from services.page_home import page_home

menu_lateral = [
    'Home',
    'Curiosidades',
    'Mapa de Inadimplência'
]

st.image('data/titulo.png')

def dashboard() -> None:
    choice = st.sidebar.selectbox('Páginas', menu_lateral)
    if choice == 'Curiosidades':
        page_curiosidades_llm()
    elif choice == 'Mapa de Inadimplência':
        page_dash()
    elif choice == 'Home':
        page_home()

if __name__ == '__main__':
    dashboard()