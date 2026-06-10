# 🛠️ Guia de Desenvolvimento

Guia completo para desenvolvedores trabalharem com o projeto.

## 📚 Índice

- [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Convenções de Código](#convenções-de-código)
- [Testes](#testes)
- [Logging](#logging)
- [Tratamento de Erros](#tratamento-de-erros)

---

## Ambiente de Desenvolvimento

### Setup Inicial

```bash
# 1. Clonar repositório
git clone https://github.com/USERNAME/academico-api.git
cd academico-api

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar servidor
uvicorn app.main:app --reload --port 8000
```

### Variáveis de Ambiente

Copiar `.env.example` para `.env`:

```bash
cp .env.example .env
```

Editar `.env` com suas configurações:

```env
DATABASE_URL=sqlite:///./academic.db
DEBUG=True
```

---

## Estrutura do Projeto

### Camadas da Aplicação

```
app/
├── main.py                 # Aplicação FastAPI
├── domain/models.py        # Entidades (ORM SQLAlchemy)
├── schemas/schemas.py      # Validação (Pydantic)
├── services/               # Lógica de negócio
├── router/                 # Endpoints HTTP
└── database/               # Banco de dados
```

### Fluxo de Requisição

```
HTTP Request
    ↓
Router (HTTP validation)
    ↓
Service (Business logic)
    ↓
Domain (Database models)
    ↓
Database (SQLite)
    ↓
Domain (Model -> DB)
    ↓
Service (Response logic)
    ↓
Router (JSON serialization)
    ↓
HTTP Response
```

---

## Convenções de Código

### Docstrings

Todas as funções e classes devem ter docstrings no formato Google:

```python
def criar_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
    """
    Criar novo aluno no banco de dados.
    
    Args:
        db: Sessão do banco de dados
        aluno: Dados do aluno a criar (AlunoCreate)
    
    Returns:
        Aluno: Objeto aluno criado com ID gerado
    
    Raises:
        HTTPException: Se email ou matrícula já existem (400)
    
    Example:
        >>> aluno_data = AlunoCreate(...)
        >>> aluno = criar_aluno(db, aluno_data)
    """
```

### Type Hints

Sempre usar type hints:

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def obter_alunos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
    """Listar alunos com paginação."""
    return db.query(Aluno).offset(skip).limit(limit).all()
```

### Naming Conventions

- **Classes**: PascalCase (`AlunoService`, `AlunoCreate`)
- **Funções**: snake_case (`criar_aluno`, `obter_alunos`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_ALUNOS`)
- **Privadas**: prefixo `_` (`_validar_email`)

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def criar_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
    try:
        # ... lógica ...
        logger.info(f"✓ Aluno criado: {aluno.nome}")
        return db_aluno
    except Exception as e:
        logger.error(f"✗ Erro ao criar aluno: {e}")
        raise
```

---

## Testes

### Estrutura

```
tests/
├── __init__.py
├── test_endpoints.py       # Testes de endpoints
├── test_services.py        # Testes de serviços
└── test_models.py          # Testes de modelos
```

### Executar Testes

```bash
# Todos os testes
pytest

# Com verbosidade
pytest -v

# Arquivo específico
pytest tests/test_endpoints.py

# Função específica
pytest tests/test_endpoints.py::TestAlunos::test_criar_aluno

# Com coverage
pytest --cov=app tests/
```

### Exemplo de Teste

```python
def test_criar_aluno():
    """Testar criação de aluno."""
    aluno_data = {
        "nome": "João Silva",
        "email": "joao@test.com",
        "matricula": "2024001",
        "periodo": 1
    }
    response = client.post("/v1/alunos", json=aluno_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "João Silva"
```

---

## Logging

### Níveis de Log

```python
logger.debug("Informação detalhada")      # DEBUG
logger.info("✓ Operação concluída")      # INFO
logger.warning("⚠️ Comportamento incomum") # WARNING
logger.error("✗ Erro na operação")       # ERROR
logger.critical("🔴 Erro crítico")       # CRITICAL
```

### Padrão de Log

```
2024-06-10 10:30:45,123 - app.services.aluno_service - INFO - ✓ Aluno criado: João Silva
```

---

## Tratamento de Erros

### Padrão de Erro

```python
from fastapi import HTTPException, status

def obter_aluno(db: Session, aluno_id: int) -> Aluno:
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    
    if not aluno:
        logger.warning(f"Aluno {aluno_id} não encontrado")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    
    return aluno
```

### Códigos HTTP Comuns

| Código | Significado | Quando Usar |
|--------|-----------|-----------|
| 200 | OK | Sucesso geral |
| 201 | Created | Recurso criado |
| 204 | No Content | Deletado com sucesso |
| 400 | Bad Request | Dados inválidos |
| 404 | Not Found | Recurso não existe |
| 409 | Conflict | Violação de constraint |
| 500 | Server Error | Erro não tratado |

---

## Git Workflow

### Commits

```bash
# Feature nova
git checkout -b feature/nome-da-feature
git add .
git commit -m "feat: adicionar nova funcionalidade"

# Bugfix
git checkout -b fix/nome-do-bug
git add .
git commit -m "fix: corrigir bug de criação"

# Documentação
git commit -m "docs: atualizar README"
```

### Merge

```bash
git checkout main
git merge feature/nome-da-feature
git push origin main
```

---

## Recursos Úteis

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [Python PEP 8](https://pep8.org/)

---

**Happy Coding! 🚀**
