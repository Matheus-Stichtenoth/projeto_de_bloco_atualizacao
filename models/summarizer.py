from transformers import pipeline
from langchain_openai.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

import os

load_dotenv('.env')

key_api_openai = os.environ["OPENAI_KEY"]
modelo_openai = 'gpt-4o'

def summarize_text_openai_estados(text: str):
    """
    Gera um resumo para o texto fornecido usando o modelo especificado.
    
    :param text: O texto a ser resumido.
    :return: O resumo gerado.
    """
    template = ChatPromptTemplate([
        ('system','''
                Você é uma ferramenta responsável por resumir artigos, textos e curiosidades sobre inadimplência.
                Traga em tópicos as principais mudanças de mercado, quando houverem comparações.
                O resultado final deve ser um texto de até 300 caracteres.
                Não utilize tópicos durante o resumo.
                Deixe claro os principais agravantes da inadimplência em cada ano, baseado no texto que você receber.
                Traga apenas dados regionais que envolvam alguma região, estado ou cidade. Caso você não encontre informações regionais, Informe a seguinte mensagem: "Não foi possível encontrar dados regionais nos dados no ano selecionado".
         '''),
        ('user','Resuma isso: {text}')
    ])
    llm = ChatOpenAI(model = modelo_openai,api_key=key_api_openai)
    response = llm.invoke(template.format_messages(text = text))
    return response.content

def summarize_text_openai_brasil(text: str):
    """
    Gera um resumo para o texto fornecido usando o modelo especificado.
    
    :param text: O texto a ser resumido.
    :return: O resumo gerado.
    """
    template = ChatPromptTemplate([
        ('system','''
                Você é uma ferramenta responsável por resumir artigos, textos e curiosidades sobre inadimplência.
                Traga em tópicos as principais mudanças de mercado, quando houverem comparações.
                O resultado final deve ser um texto de até 300 caracteres.
                Não utilize tópicos durante o resumo.
                Deixe claro os principais agravantes da inadimplência em cada ano, baseado no texto que você receber.
                Traga apenas dados gerais do Brasil, sem citar nenhum estado, região ou cidade.       
         '''),
        ('user','Resuma isso: {text}')
    ])
    llm = ChatOpenAI(model = modelo_openai,api_key=key_api_openai)
    response = llm.invoke(template.format_messages(text = text))
    return response.content