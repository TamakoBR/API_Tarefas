
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


DB_PATH = Path(__file__).resolve().parent / "tarefas.db"


@contextmanager
def conectar() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row

    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


def criar_tabela():
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL
                    CHECK(length(trim(titulo)) BETWEEN 1 AND 100),
                descricao TEXT,
                concluida INTEGER NOT NULL DEFAULT 0
                    CHECK(concluida IN (0, 1))
            )
        """)


def converter_tarefa(linha):
    if linha is None:
        return None

    return {
        "id": linha["id"],
        "titulo": linha["titulo"],
        "descricao": linha["descricao"],
        "concluida": bool(linha["concluida"]),
    }


def listar_tarefas():
    with conectar() as conexao:
        linhas = conexao.execute("""
            SELECT id, titulo, descricao, concluida
            FROM tarefas
            ORDER BY id
        """).fetchall()

        return [converter_tarefa(linha) for linha in linhas]


def criar_tarefa(titulo, descricao):
    with conectar() as conexao:
        cursor = conexao.execute("""
            INSERT INTO tarefas (titulo, descricao)
            VALUES (?, ?)
        """, (titulo, descricao))

        linha = conexao.execute("""
            SELECT id, titulo, descricao, concluida
            FROM tarefas
            WHERE id = ?
        """, (cursor.lastrowid,)).fetchone()

        return converter_tarefa(linha)


def atualizar_tarefa(tarefa_id, titulo, descricao, concluida):
    with conectar() as conexao:
        cursor = conexao.execute("""
            UPDATE tarefas
            SET titulo = ?, descricao = ?, concluida = ?
            WHERE id = ?
        """, (titulo, descricao, int(concluida), tarefa_id))

        if cursor.rowcount == 0:
            return None

        linha = conexao.execute("""
            SELECT id, titulo, descricao, concluida
            FROM tarefas
            WHERE id = ?
        """, (tarefa_id,)).fetchone()

        return converter_tarefa(linha)


def excluir_tarefa(tarefa_id):
    with conectar() as conexao:
        cursor = conexao.execute("""
            DELETE FROM tarefas
            WHERE id = ?
        """, (tarefa_id,))

        return cursor.rowcount > 0
