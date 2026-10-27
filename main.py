
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import criar_tabela
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabela()
    yield


app = FastAPI(
    title="API de Tarefas",
    description="API para cadastro e gerenciamento de tarefas.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/")
def inicio():
    return {"mensagem": "API de tarefas funcionando!"}
