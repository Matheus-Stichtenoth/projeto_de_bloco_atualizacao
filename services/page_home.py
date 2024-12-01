import streamlit as st

def page_home():

    st.subheader('O seu portal de dados de inadimplência no Brasil!')

    st.image('data/capa_riskmap.png')

    st.subheader('Para uma melhor experiência, utilize o formato "Wide" da tela, clicando em "Settings" e habilitando a opção.', divider='red')

    desenvolvedor, instituicao = st.columns(2)

    with desenvolvedor:
        st.write('Desenvolvido por Matheus de Oliveira Stichtenoth.')

    with instituicao:
        st.write('Aplicado na instituição INFNET.')

    linkedin_logo, linkedin_link, email_logo, email_link = st.columns(4)

    with linkedin_logo:
        st.image('data/linkedin_logo.png', width=75)

    with linkedin_link:
        st.write('/in/matheus-stichtenoth/')

    with email_logo:
        st.image('data/email_logo.png', width=75)

    with email_link:
        st.write('matheus.o.stichtenoth@gmail.com.br')