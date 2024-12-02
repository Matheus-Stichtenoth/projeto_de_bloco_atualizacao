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
from services.page_dash_estado import page_dash_estado

menu_lateral = [
    'Home 🏠',
    'Curiosidades (LLM) 🔎',
    'Dashboard - Visão Brasil 🗺',
    'Dashboard - Visão Mensal por Estado 🧩'
]

st.image('data/titulo.png')

def dashboard() -> None:
    choice = st.sidebar.selectbox('Páginas', menu_lateral)
    if choice == 'Curiosidades (LLM) 🔎':
        page_curiosidades_llm()
    elif choice == 'Dashboard - Visão Brasil 🗺':
        page_dash()
    elif choice == 'Home 🏠':
        page_home()
    elif choice == 'Dashboard - Visão Mensal por Estado 🧩':
        page_dash_estado()

if __name__ == '__main__':
    dashboard()