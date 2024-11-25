import streamlit as st
import pandas as pd
import plotly.express as px
import json
from src.utils import fetch_bcb_data, load_local_backup, calculate_indebtedness

def page_dash():
    ##CRIANDO DATAFRAMES##

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

    #INADIMPLENCIA TOTAL
    valores_totais = df[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    inad_total = valores_totais['VENCIDO_ACIMA_DE_15_DIAS'] / valores_totais['CARTEIRA']
    inad_total_metric = f'{inad_total:.2%}'

    #INADIMPLENCIA POR ESTADO
    df_uf = df.groupby('ESTADO', as_index=False)[['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']].sum()
    df_uf['Inadimplencia'] = (df_uf['VENCIDO_ACIMA_DE_15_DIAS'] / df_uf['CARTEIRA']) *100
    df_uf = df_uf.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    #INADIMPLENCIA POR CLIENTE
    df_cliente = df.groupby('CLIENTE')[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    df_cliente['INADIMPLENCIA'] = (df_cliente['VENCIDO_ACIMA_DE_15_DIAS'] / df_cliente['CARTEIRA']) * 100
    df_cliente.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    #INADIMPLENCIA POR MODALIDADE
    df_modalidade = df.groupby('MODALIDADE')[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    df_modalidade['INADIMPLENCIA'] = (df_modalidade['VENCIDO_ACIMA_DE_15_DIAS']/df_modalidade['CARTEIRA']) *100
    df_modalidade.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    ##CRIANDO GRÁFICOS##
    # Criar o mapa coroplético
    fig = px.choropleth(
        df_uf,
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