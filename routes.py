
from fastapi import APIRouter, HTTPException, Response

import database
from models import TarefaCreate, TarefaUpdate


router = APIRouter(tags=["tarefas"])


@router.get("/tarefas")
def listar_tarefas():
    return database.listar_tarefas()


@router.post("/tarefas", status_code=201)
def criar_tarefa(tarefa: TarefaCreate):
    return database.criar_tarefa(
        tarefa.titulo,
        tarefa.descricao,
    )


@router.put("/tarefas/{tarefa_id}")
def atualizar_tarefa(
    tarefa_id: int,
    tarefa: TarefaUpdate,
):
    tarefa_atualizada = database.atualizar_tarefa(
        tarefa_id,
        tarefa.titulo,
        tarefa.descricao,
        tarefa.concluida,
    )

    if tarefa_atualizada is None:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada",
        )

    return tarefa_atualizada


@router.delete(
    "/tarefas/{tarefa_id}",
    status_code=204,
    response_class=Response,
)
def deletar_tarefa(tarefa_id: int) -> Response:
    excluida = database.excluir_tarefa(tarefa_id)

    if not excluida:
        raise HTTPException(
            status_code=404,
            detail="Tarefa não encontrada",
        )

    return Response(status_code=204)
