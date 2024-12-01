from transformers import pipeline
import streamlit as st
import pandas as pd
from models.summarizer import summarize_text_openai_brasil, summarize_text_openai_estados

def page_curiosidades_llm():
    @st.cache_data
    def carregar_dados(filepath: str):
        return pd.read_csv(filepath, encoding = 'utf-8')

    def filtrar_por_ano(df, ano):
        df["Ano"] = df["Mês"].str.extract(r"(\d{4})")  # Extrai o ano do campo "Mês"
        return df[df["Ano"] == str(ano)]

    def dividir_texto(texto, max_words=400):
        """
        Divide o texto em blocos de no máximo `max_words` palavras.
        """
        palavras = texto.split()
        for i in range(0, len(palavras), max_words):
            yield " ".join(palavras[i:i + max_words])

    def resumir_bloco(bloco, summarizer, max_length=250):
        """
        Resume um único bloco de texto.
        """
        return summarizer(bloco, max_length=max_length, min_length=150, do_sample=False)[0]["summary_text"]

    def resumo_final_brasil(texto, summarizer, progress_bar):
        """
        Realiza o processo de resumo em múltiplas camadas:
        1. Divide o texto em blocos de 1024 palavras.
        2. Resume cada bloco.
        3. Concatena os resumos e gera um resumo final.
        """
        blocos = list(dividir_texto(texto))
        total_blocos = len(blocos)
        resumos_parciais = []

        # Primeira camada: Resumir cada bloco
        for idx, bloco in enumerate(blocos):
            resumo_parcial = resumir_bloco(bloco, summarizer)
            resumos_parciais.append(resumo_parcial)
            progress_bar.progress(int(((idx + 1) / (total_blocos + 1)) * 100))  # Atualiza barra de progresso

        # Concatenar os resumos dos blocos
        texto_concatenado = " ".join(resumos_parciais)

        # Segunda camada: Resumir o texto concatenado
        resumo_final = summarize_text_openai_brasil(text = texto_concatenado)
        progress_bar.progress(100)  # Finaliza a barra de progresso

        return resumo_final
    
    def resumo_final_estados(texto, summarizer, progress_bar):
        """
        Realiza o processo de resumo em múltiplas camadas:
        1. Divide o texto em blocos de 1024 palavras.
        2. Resume cada bloco.
        3. Concatena os resumos e gera um resumo final.
        """
        blocos = list(dividir_texto(texto))
        total_blocos = len(blocos)
        resumos_parciais = []

        # Primeira camada: Resumir cada bloco
        for idx, bloco in enumerate(blocos):
            resumo_parcial = resumir_bloco(bloco, summarizer)
            resumos_parciais.append(resumo_parcial)
            progress_bar.progress(int(((idx + 1) / (total_blocos + 1)) * 100))  # Atualiza barra de progresso

        # Concatenar os resumos dos blocos
        texto_concatenado = " ".join(resumos_parciais)

        # Segunda camada: Resumir o texto concatenado
        resumo_final = summarize_text_openai_estados(text = texto_concatenado)
        progress_bar.progress(100)  # Finaliza a barra de progresso

        return resumo_final

    st.title("Curiosidades de Inadimplência")

    filepath = "data/informacoes_inadimplencia.csv"  # Atualize conforme necessário
    df = carregar_dados(filepath)

    anos_disponiveis = ["2021", "2022", "2023", "2024"]
    ano_selecionado = st.selectbox("Selecione o ano para resumir as informações:", anos_disponiveis)

    dados_filtrados = filtrar_por_ano(df, ano_selecionado)

    c1, c2 = st.columns(2)

    with c1:
        st.write("""
                 As curiosidades observadas ao lado direito foram extraídas do Serasa. \n
                 Todo mês o Serasa libera as principais informações da inadimplência no Brasil referente à esse mês. \n
                 Para facilitar, já fiz o resumo desses dados para você :) \n
                 Na tabela ao lado, você pode observar as curiosidades por ano, e abaixo, você pode fazer o download das curiosidades. \n
                 Ao final da página, você têm a possibilidade de resumir as curiosidades daquele ano. Vamos tentar? Clique no botão para gerar o resumo.
                 """)

    with c2:
        dados_filtrados_plot = dados_filtrados.rename(columns={'conteudo': 'Curiosidades'})
        st.dataframe(dados_filtrados_plot)

    df_filtered, df_full = st.columns(2)

    with df_filtered:
        st.download_button(
            label=f'Clique aqui para baixar as curiosidades de inadimplência de {ano_selecionado}.',
            data=dados_filtrados.to_csv(index=False),
            file_name=f'curiosidades_inadimplencia_{ano_selecionado}.csv'
        )
        
    with df_full:
        st.download_button(
            label='Clique aqui para baixar todas as curiosidades de inadimplência.',
            data=df.to_csv(index=False),
            file_name=f'curiosidades_inadimplencia.csv'
        )

    st.markdown("<h1 style='text-align: center; color: #8084a2;'>Uso de LMM para resumo de curiosidades 🔎</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #575a6e;'>Selecione abaixo a opção de resumo das curiosidades: </h2>", unsafe_allow_html=True)
    c1_regioes, c2_brasil = st.columns(2)

    with c2_brasil: 
        if st.button(f'Resumo Nacional em {ano_selecionado}',key='resumo_brasil'):
            texto_completo = " ".join(dados_filtrados["conteudo"].tolist())

            with st.spinner('Gerando resumo, por favor aguarde... isso pode levar alguns segundos.'):
                
                progress_bar = st.progress(0)

                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

                resumo_final = resumo_final_brasil(texto_completo, summarizer, progress_bar)

            # Exibir o resumo
            st.subheader("Resumo das Informações:")
            st.text(resumo_final)

    with c1_regioes:
        if st.button(f'Resumo por Regiões e Estados em {ano_selecionado}', key = 'resumo_estados'):
            texto_completo = " ".join(dados_filtrados["conteudo"].tolist())

            with st.spinner('Gerando resumo, por favor aguarde... isso pode levar alguns segundos.'):
                
                progress_bar = st.progress(0)

                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

                resumo_final = resumo_final_estados(texto_completo, summarizer, progress_bar)

            # Exibir o resumo
            st.subheader("Resumo das Informações:")
            st.text(resumo_final)