import streamlit as st
import pandas as pd
import plotly.express as px
import json
from src.utils import fetch_bcb_data, load_local_backup, calculate_indebtedness

def page_map():
    # Carregar os dados
    try:
        df = fetch_bcb_data()
    except:
        df = load_local_backup()

    df = calculate_indebtedness(df)

    # Carregar o arquivo GeoJSON dos estados brasileiros
    with open('data/brazil-states.geojson', 'r') as file:
        geojson_data = json.load(file)

    # Carregar os dados de inadimplência
    df = pd.read_json('data/api_data.json')

    # Preprocessar os dados para calcular a taxa de inadimplência por estado
    df['Inadimplencia'] = df['VENCIDO_ACIMA_DE_15_DIAS'] / df['CARTEIRA']
    df_state = df.groupby('ESTADO', as_index=False)['Inadimplencia'].mean()

    # Criar o mapa coroplético
    fig = px.choropleth(
        df_state,
        geojson=geojson_data,
        locations='ESTADO',
        featureidkey='properties.sigla',  # Mapeia o código UF do GeoJSON
        color='Inadimplencia',
        color_continuous_scale='Reds',
        title='Taxa de Inadimplência por Estado',
        labels={'Inadimplencia': 'Inadimplência (%)'}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    # Exibir o gráfico no Streamlit
    st.title("Mapa de Inadimplência")
    st.plotly_chart(fig)