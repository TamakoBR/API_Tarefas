## Como rodar

1. Crie e ative o ambiente virtual:
   `python -m venv .venv` e depois `.venv\Scripts\activate` (Windows)
2. Instale as dependências: `pip install -r requirements.txt`
3. Inicie a API: `uvicorn main:app --reload`
4. Acesse a documentação interativa em `http://localhost:8000/docs`

## Rotas

- `GET /` : verifica se a API está funcionando
- `GET /tarefas` : lista as tarefas
- `POST /tarefas` : cria uma tarefa

## Tecnologias

Python, FastAPI, Pydantic

## Próximos passos

- Rotas para editar e apagar tarefas
- Banco de dados SQLite
- Testes automatizados com pytest