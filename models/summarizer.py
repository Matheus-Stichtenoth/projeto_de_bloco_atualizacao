from transformers import pipeline
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

import os

load_dotenv('.env')

key_api_openai = os.environ["OPENAI_KEY"]
modelo_openai = 'gpt-4o'

def summarize_text(text: str):
    """
    Gera um resumo para o texto fornecido usando o modelo especificado.
    
    :param text: O texto a ser resumido.
    :return: O resumo gerado.
    """
    summarizer = pipeline("summarization", model='facebook/bart-large-cnn')
    summary = summarizer(text, do_sample=False)
    return summary[0]["summary_text"]

def summarize_text_openai(text: str):
    """
    Gera um resumo para o texto fornecido usando o modelo especificado.
    
    :param text: O texto a ser resumido.
    :return: O resumo gerado.
    """
    template = ChatPromptTemplate([
        ('system','''
                Você é uma ferramenta responsável por resumir artigos, textos e curiosidades sobre inadimplência.
                Traga em tópicos as principais mudanças de mercado, quando houverem comparações.
                Deixe claro os principais agravantes da inadimplência em cada ano, baseado no texto que você receber.
                '''),
        ('user','Traduza isso: {text}')
    ])
    llm = ChatOpenAI(model = modelo_openai,api_key=key_api_openai)
    response = llm.invoke(template.format_messages(text = text))
    return response.content