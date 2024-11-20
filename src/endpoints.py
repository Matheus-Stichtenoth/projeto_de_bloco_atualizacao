from fastapi import FastAPI
from routers.dados_endpoints import router as dados_router

app = FastAPI()

# Inclua os endpoints do novo arquivo
app.include_router(dados_router, prefix="/dados")
