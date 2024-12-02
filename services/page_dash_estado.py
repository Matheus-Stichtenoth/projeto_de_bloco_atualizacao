import streamlit as st
import pandas as pd
import plotly.express as px
import json
from src.utils import fetch_bcb_data, load_local_backup, calculate_indebtedness
from matplotlib import pyplot as plt
import subprocess
from plotly import express as px

def page_dash_estado():
    ##CRIANDO DATAFRAMES##

    try:
        df = fetch_bcb_data()
    except:
        df = load_local_backup()

    estados = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS",
    "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC",
    "SE", "SP", "TO"
    ]

    estado_selecionado = st.selectbox('Selecione o Estado que deseja fazer a annálise:',estados)

    df = df[df['ESTADO'] == estado_selecionado]
    df['Date'] = pd.to_datetime(df['DATA_BASE'], format='%Y%m')

    #INADIMPLENCIA TOTAL
    valores_totais = df[['CARTEIRA','VENCIDO_ACIMA_DE_15_DIAS']].sum()
    inad_total = valores_totais['VENCIDO_ACIMA_DE_15_DIAS'] / valores_totais['CARTEIRA']
    inad_total_metric = f'{inad_total:.2%}'

    #MEDIA DE INADIMPLENCIA POR MES
    df_mes = df.groupby(['DATA_BASE','Date'],as_index=False)[['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']].sum()
    df_mes['INADIMPLENCIA'] = (df_mes['VENCIDO_ACIMA_DE_15_DIAS'] / df_mes['CARTEIRA']) * 100
    df_mes_mean = df_mes['INADIMPLENCIA'].mean()
    df_mes_mean_metric = f'{(df_mes_mean/100):.2%}'

    #MES COM MENOR INADIMPLENCIA
    df_mes_min= df_mes[df_mes['INADIMPLENCIA'] == df_mes['INADIMPLENCIA'].min()]
    df_mes_min = df_mes_min.reset_index(drop=True)  # Redefinir índice
    df_mes_min_metric = f'{df_mes_min["INADIMPLENCIA"].iloc[0]:.2f}%'
    df_mes_min_metric_data = f'{df_mes_min["DATA_BASE"].iloc[0]}'


    #MES COM MAIOR INADIMPLENCIA
    df_mes_max = df_mes[df_mes['INADIMPLENCIA'] == df_mes['INADIMPLENCIA'].max()]
    df_mes_max = df_mes_max.reset_index(drop=True)  # Redefinir índice
    df_mes_max_metric = f'{df_mes_max["INADIMPLENCIA"].iloc[0]:.2f}%'
    df_mes_max_metric_data = f'{df_mes_max["DATA_BASE"].iloc[0]}'

    #INADIMPLENCIA POR MODALIDADES
    df_modalidade = df.groupby(['Date','MODALIDADE'],as_index=False)[['VENCIDO_ACIMA_DE_15_DIAS','CARTEIRA']].sum()
    df_modalidade['INADIMPLENCIA'] = (df_modalidade['VENCIDO_ACIMA_DE_15_DIAS'] / df_modalidade['CARTEIRA']) * 100

    with st.container():
        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c2.metric(label=f'Inadimplência Total do {estado_selecionado}', value=inad_total_metric)
        c3.metric(label='Média de Inadimplência Mensal',value=df_mes_mean_metric)
        c4.metric(label='Mês com Maior Inadimplência',value=df_mes_max_metric, 
                  delta=df_mes_max_metric_data, delta_color='off')
        c5.metric(label='Mês com Menor Inadimplência',value=df_mes_min_metric, 
                  delta=df_mes_min_metric_data, delta_color='off')


    st.markdown(f"<h3 style='text-align: center; color: #ffffff;'>Evolução da Inadimplência Nos Últimos 12 Meses no {estado_selecionado}</h3>", unsafe_allow_html=True)
    fig_bar = px.bar(
            df_mes,
            x = 'Date',
            y = 'INADIMPLENCIA',
            text_auto=True,
            color_discrete_sequence=["#f5543c"]
    )
    fig_bar.update_traces(textfont_size=16, textposition="outside")
    st.plotly_chart(fig_bar)

    st.markdown(f"<h3 style='text-align: center; color: #ffffff;'>Evolução da Inadimplência por Modalidade no {estado_selecionado}</h3>", unsafe_allow_html=True)
        
    fig_line = px.line(
            df_modalidade,
            x = 'Date',
            y = 'INADIMPLENCIA',
            color = 'MODALIDADE',
            symbol= 'MODALIDADE'
    )

    fig_line.update_traces(textfont_size=16, textposition="top center")
    st.plotly_chart(fig_line)