
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="API de Tarefas",
    description="API para cadastro e gerenciamento de tarefas.",
    version="0.1.0",
)


# Dados necessários para criar uma tarefa
class TarefaCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descricao: str | None = None


# Dados necessários para atualizar uma tarefa
class TarefaUpdate(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descricao: str | None = None
    concluida: bool


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


@app.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(tarefa_id: int, tarefa: TarefaUpdate):
    for i, t in enumerate(tarefas):
        if t["id"] == tarefa_id:
            tarefas[i] = {
                "id": tarefa_id,
                "titulo": tarefa.titulo,
                "descricao": tarefa.descricao,
                "concluida": tarefa.concluida,
            }

            return tarefas[i]

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada",
    )


@app.delete(
    "/tarefas/{tarefa_id}",
    status_code=204,
    response_class=Response,
)
def deletar_tarefa(tarefa_id: int) -> Response:
    for i, t in enumerate(tarefas):
        if t["id"] == tarefa_id:
            tarefas.pop(i)
            return Response(status_code=204)

    raise HTTPException(
        status_code=404,
        detail="Tarefa não encontrada",
    )
