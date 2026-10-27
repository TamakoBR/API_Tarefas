
from pydantic import BaseModel, Field, field_validator


class TarefaBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)
    descricao: str | None = Field(default=None, max_length=500)

    @field_validator("titulo")
    @classmethod
    def validar_titulo(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError(
                "O título não pode conter apenas espaços."
            )

        return valor


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(TarefaBase):
    concluida: bool
