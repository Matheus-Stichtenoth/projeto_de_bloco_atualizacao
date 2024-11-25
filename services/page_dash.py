import streamlit as st
import pandas as pd
import plotly.express as px
import json
from src.utils import fetch_bcb_data, load_local_backup, calculate_indebtedness
from matplotlib import pyplot as plt

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
    df = df[df['ESTADO'] != 'NI']

    #INADIMPLENCIA TOTAL
    valores_totais = df[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    inad_total = valores_totais['VENCIDO_ACIMA_DE_15_DIAS'] / valores_totais['CARTEIRA']
    inad_total_metric = f'{inad_total:.2%}'

    #INADIMPLENCIA POR ESTADO
    df_uf = df.groupby('ESTADO', as_index=False)[['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']].sum()
    df_uf['INADIMPLENCIA'] = (df_uf['VENCIDO_ACIMA_DE_15_DIAS'] / df_uf['CARTEIRA']) *100
    df_uf = df_uf.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    #INADIMPLENCIA POR ESTADO - MAIOR INADIMPLENCIA DO BRASIL
    df_uf_max = df_uf[df_uf['INADIMPLENCIA'] == df_uf['INADIMPLENCIA'].max()]
    df_uf_max = df_uf_max.reset_index(drop=True)  # Redefinir índice
    df_uf_max_metric = f'{df_uf_max["INADIMPLENCIA"].iloc[0]:.2f}%'
    df_uf_max_metric_uf = f'{df_uf_max["ESTADO"].iloc[0]}'

    #INADIMPLENCIA POR ESTADO - MENOR INADIMPLENCIA DO BRASIL
    df_uf_min = df_uf[df_uf['INADIMPLENCIA'] == df_uf['INADIMPLENCIA'].min()]
    df_uf_min = df_uf_min.reset_index(drop=True)  # Redefinir índice
    df_uf_min_metric = f'{df_uf_min["INADIMPLENCIA"].iloc[0]:.2f}%'
    df_uf_min_metric_uf = f'{df_uf_min["ESTADO"].iloc[0]}'

    #INADIMPLENCIA POR ESTADO - MÉDIA INADIMPLENCIA DO BRASIL
    df_uf_mean = df_uf['INADIMPLENCIA'].mean()
    df_uf_mean_metric = f'{(df_uf_mean/100):.2%}'

    ##INADIMPLENCIA POR ESTADO - DELTA MAX PRA MEDIA
    delta_max_mean = df_uf_max["INADIMPLENCIA"].iloc[0] - df_uf_mean

    ##INADIMPLENCIA POR ESTADO - DELTA MIN PRA MEDIA
    delta_min_mean = df_uf_min["INADIMPLENCIA"].iloc[0] - df_uf_mean

    #INADIMPLENCIA POR CLIENTE
    df_cliente = df.groupby('CLIENTE')[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    df_cliente['INADIMPLENCIA'] = (df_cliente['VENCIDO_ACIMA_DE_15_DIAS'] / df_cliente['CARTEIRA']) * 100
    df_cliente.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    #INADIMPLENCIA POR MODALIDADE
    df_modalidade = df.groupby('MODALIDADE')[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    df_modalidade['INADIMPLENCIA'] = (df_modalidade['VENCIDO_ACIMA_DE_15_DIAS']/df_modalidade['CARTEIRA']) *100
    df_modalidade.drop(columns=['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']).sort_values('INADIMPLENCIA',ascending=False)

    ##CRIANDO COLUNAS E CONTAINERS
    with st.container():
        c1, c2, c3, c4 = st.columns(4)

        c1.metric(label='Inadimplência Total do Brasil', value=inad_total_metric)
        c2.metric(label='Média de Inadimplência por Estado', value=df_uf_mean_metric)
        c3.metric(label='Maior Inadimplência de um Estado', value=df_uf_max_metric, 
                  delta= f'{(delta_max_mean/100):.2%} - {df_uf_max_metric_uf}',delta_color='inverse')
        c4.metric(label='Menor Inadimplência de um Estado', value=df_uf_min_metric, 
                  delta= f'{(delta_min_mean/100):.2%} - {df_uf_min_metric_uf}',delta_color='inverse')

    ##CRIANDO GRÁFICOS##
    # Criar o mapa coroplético

    plt.figure(figsize=(30,30))

    fig = px.choropleth(
        df_uf,
        geojson=geojson_data,
        locations='ESTADO',
        featureidkey='properties.sigla',  # Mapeia o código UF do GeoJSON
        color='INADIMPLENCIA',
        color_continuous_scale='Reds',
        title='Taxa de Inadimplência por Estado',
        labels={'INADIMPLENCIA': 'Inadimplência (%)'}
    )

    fig.update_geos(
        fitbounds="locations",
        visible=False
    )

    # Exibir o gráfico no Streamlit
    st.title("Mapa de Inadimplência")
    st.plotly_chart(fig)