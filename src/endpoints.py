from fastapi import FastAPI, HTTPException
from routers.dados_endpoints import router as dados_router
import json
from pathlib import Path

app = FastAPI()

# Inclua os endpoints do novo arquivo
app.include_router(dados_router, prefix="/dados")

DATA_PATH = Path("data/api_data.json")

@app.get("/dados", summary="Retorna os dados do arquivo JSON")
async def get_dados():
    """
    Endpoint para retornar os dados do arquivo api_data.json.
    """
    if not DATA_PATH.exists():
        raise HTTPException(status_code=404, detail="Arquivo api_data.json não encontrado.")
    
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar o arquivo JSON: {str(e)}")
