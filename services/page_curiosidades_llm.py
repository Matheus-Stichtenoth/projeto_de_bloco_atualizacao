from transformers import pipeline
import streamlit as st
import pandas as pd

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

    def gerar_resumo_final(texto, summarizer, progress_bar):
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
        resumo_final = resumir_bloco(texto_concatenado, summarizer)
        progress_bar.progress(100)  # Finaliza a barra de progresso

        return resumo_final

    # Configuração do Streamlit
    st.title("Curiosidades de Inadimplência")

    # Carregar os dados
    filepath = "data/informacoes_inadimplencia.csv"  # Atualize conforme necessário
    df = carregar_dados(filepath)

    # Seleção do ano pelo usuário
    anos_disponiveis = ["2021", "2022", "2023", "2024"]
    ano_selecionado = st.selectbox("Selecione o ano para resumir as informações:", anos_disponiveis)

    # Filtrar os dados pelo ano selecionado
    dados_filtrados = filtrar_por_ano(df, ano_selecionado)

    st.dataframe(dados_filtrados)

    # Botões de download
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

    # Sumarização com barra de progresso
    if st.button(f'Clique aqui para realizar um resumo das curiosidades de inadimplência em {ano_selecionado}'):
        # Concatenar os textos do ano selecionado
        texto_completo = " ".join(dados_filtrados["conteudo"].tolist())

        with st.spinner('Gerando resumo, por favor aguarde... isso pode levar alguns segundos.'):
            # Inicializar a barra de progresso
            progress_bar = st.progress(0)

            # Carregar o modelo de sumarização
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

            # Gerar o resumo em camadas
            resumo_final = gerar_resumo_final(texto_completo, summarizer, progress_bar)

        # Exibir o resumo
        st.subheader("Resumo das Informações:")
        st.text(resumo_final)