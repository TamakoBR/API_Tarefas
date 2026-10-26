
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API de Tarefas",
    description="API para cadastro e gerenciamento de tarefas.",
    version="0.1.0",
)


# Modelo dos dados recebidos ao criar uma tarefa
class TarefaCreate(BaseModel):
    titulo: str
    descricao: str | None = None


# Armazenamento temporário em memória
tarefas = []
proximo_id = 1


@app.get("/")
def inicio():
    return {"mensagem": "API de tarefas funcionando!"}


@app.get("/tarefas")
def listar_tarefas():
    return tarefas


@app.post("/tarefas", status_code=201)
def criar_tarefa(tarefa: TarefaCreate):
    global proximo_id

    nova_tarefa = {
        "id": proximo_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": False,
    }

    tarefas.append(nova_tarefa)
    proximo_id += 1

    return nova_tarefa
