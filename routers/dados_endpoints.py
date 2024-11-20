from fastapi import APIRouter, HTTPException
from models.input_dados_api import InputDadosAPI
from typing import List

router = APIRouter()

# Simula um banco de dados na memória
dados_memoria = []

@router.post("/adicionar_dados")
async def adicionar_dados(dados: List[InputDadosAPI]):
    """
    Endpoint para adicionar novos dados. Recebe uma lista de objetos no formato JSON,
    valida cada entrada com o modelo `InputDadosAPI`, e armazena na memória.
    """
    try:
        for dado in dados:
            dados_memoria.append(dado.dict())
        return {"message": "Dados adicionados com sucesso!", "total_registros_adicionados": len(dados)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao adicionar dados: {str(e)}")