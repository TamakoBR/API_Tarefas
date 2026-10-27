
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="API de Tarefas",
    description="API para cadastro e gerenciamento de tarefas.",
    version="0.1.0",
)


# Modelo dos dados recebidos ao criar uma tarefa
class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
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

@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaCreate):
    for i, t in enumerate(tarefas):
        if t["id"] == tarefa_id:
            tarefas[i] = {
                "id": tarefa_id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": t["concluida"],
            }
            return tarefas[i]
    return {"error": "Tarefa não encontrada"}

@app.delete("/tarefas/{tarefa_id}", status_code=204)
def deletar_tarefa(tarefa_id: int):
    for i, t in enumerate(tarefas):
        if t["id"] == tarefa_id:
            tarefas.pop(i)
            return
    return {"error": "Tarefa não encontrada"}