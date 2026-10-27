
import pytest
from fastapi.testclient import TestClient

import database
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Cada teste recebe um banco temporário isolado.
    caminho_teste = tmp_path / "teste_tarefas.db"
    monkeypatch.setattr(database, "DB_PATH", caminho_teste)

    with TestClient(app) as cliente:
        yield cliente


def test_inicio(client):
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "mensagem": "API de tarefas funcionando!"
    }


def test_criar_e_listar_tarefa(client):
    resposta = client.post(
        "/tarefas",
        json={
            "titulo": "Estudar FastAPI",
            "descricao": "Aprender testes",
        },
    )

    assert resposta.status_code == 201
    assert resposta.json()["titulo"] == "Estudar FastAPI"
    assert resposta.json()["concluida"] is False

    lista = client.get("/tarefas")

    assert lista.status_code == 200
    assert len(lista.json()) == 1


def test_rejeitar_titulo_com_espacos(client):
    resposta = client.post(
        "/tarefas",
        json={"titulo": "   "},
    )

    assert resposta.status_code == 422


def test_atualizar_tarefa(client):
    criada = client.post(
        "/tarefas",
        json={"titulo": "Tarefa original"},
    )

    tarefa_id = criada.json()["id"]

    resposta = client.put(
        f"/tarefas/{tarefa_id}",
        json={
            "titulo": "Tarefa atualizada",
            "descricao": "Atualização de teste",
            "concluida": True,
        },
    )

    assert resposta.status_code == 200
    assert resposta.json()["titulo"] == "Tarefa atualizada"
    assert resposta.json()["concluida"] is True


def test_atualizar_tarefa_inexistente(client):
    resposta = client.put(
        "/tarefas/999",
        json={
            "titulo": "Tarefa",
            "descricao": None,
            "concluida": True,
        },
    )

    assert resposta.status_code == 404


def test_excluir_tarefa(client):
    criada = client.post(
        "/tarefas",
        json={"titulo": "Tarefa para excluir"},
    )

    tarefa_id = criada.json()["id"]

    resposta = client.delete(f"/tarefas/{tarefa_id}")

    assert resposta.status_code == 204
    assert client.get("/tarefas").json() == []


def test_excluir_tarefa_inexistente(client):
    resposta = client.delete("/tarefas/999")

    assert resposta.status_code == 404
