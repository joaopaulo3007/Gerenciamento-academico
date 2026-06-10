# 🎓 API de Gerenciamento Acadêmico

Uma API REST robusta e bem documentada para gerenciar sistemas acadêmicos com suporte completo a alunos, professores, disciplinas, turmas, matrículas e notas.

**Stack**: FastAPI + SQLite + Docker + Pytest  
**Arquitetura**: Camadas (Domain, Services, Router, Database)  
**Status**: ✅ Produção-Ready

---

## ✨ Características

✅ **CRUD Completo** para Alunos e Disciplinas  
✅ **Gestão de Matrículas** - criar, cancelar, consultar com validação de vagas  
✅ **Gestão de Notas** - lançar, corrigir, consultar  
✅ **Relatórios** - boletim do aluno com médias por disciplina  
✅ **Health Check** - status da API e conexão com banco  
✅ **Swagger/OpenAPI** - documentação automática em `/docs`  
✅ **Seed de Dados** - 5 alunos, 3 professores, 4 disciplinas com notas  
✅ **Docker** - Dockerfile com health checks e docker-compose  
✅ **Validação** - schemas Pydantic com validação automática  
✅ **Logging** - logging estruturado em todos os endpoints  
✅ **Testes** - testes unitários com pytest  
✅ **Type Hints** - type annotations completas  
✅ **Docstrings** - documentação em estilo Google  

---

## 🚀 Quick Start com Docker

### Pré-requisitos
- Docker e Docker Compose instalados
- Git (opcional)

### Executar

```bash
# 1. Clonar ou entrar no diretório
git clone <seu-repositorio>
cd academico-api

# 2. Subir tudo em um comando
docker-compose up --build

# 3. API pronta! 🎉
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

A primeira execução criará o banco de dados e populará com dados de exemplo.

---

## 📚 Exemplos de Uso

### 1. Criar um Aluno

```bash
curl -X POST http://localhost:8000/v1/alunos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Paulo Felisardo",
    "email": "joaopaulodemoraesfelisardo@gmail.com",
    "matricula": "2301045",
    "periodo": 1
  }'
```

### 2. Listar Alunos

```bash
curl http://localhost:8000/v1/alunos
```

### 3. Criar Matrícula

```bash
curl -X POST http://localhost:8000/v1/matriculas \
  -H "Content-Type: application/json" \
  -d '{
    "aluno_id": 1,
    "turma_id": 1
  }'
```

### 4. Lançar Nota

```bash
curl -X POST http://localhost:8000/v1/notas \
  -H "Content-Type: application/json" \
  -d '{
    "matricula_id": 1,
    "tipo": "N1",
    "valor": 8.5
  }'
```

### 5. Consultar Boletim do Aluno

```bash
curl http://localhost:8000/v1/relatorios/boletim/1
```

### 6. Health Check

```bash
curl http://localhost:8000/v1/health
```

---

## 📖 Endpoints Principais

### Alunos (`/v1/alunos`)
- `POST /` - Criar aluno
- `GET /` - Listar alunos (paginado)
- `GET /{id}` - Obter aluno por ID
- `PUT /{id}` - Atualizar aluno
- `DELETE /{id}` - Deletar aluno

### Professores (`/v1/professores`)
- `POST /` - Criar professor
- `GET /` - Listar professores
- `GET /{id}` - Obter professor
- `PUT /{id}` - Atualizar professor
- `DELETE /{id}` - Deletar professor

### Disciplinas (`/v1/disciplinas`)
- `POST /` - Criar disciplina
- `GET /` - Listar disciplinas
- `GET /{id}` - Obter disciplina
- `PUT /{id}` - Atualizar disciplina
- `DELETE /{id}` - Deletar disciplina

### Matrículas (`/v1/matriculas`)
- `POST /` - Criar matrícula
- `GET /` - Listar matrículas
- `GET /{id}` - Obter matrícula
- `GET /aluno/{aluno_id}` - Matrículas de um aluno
- `POST /{id}/cancelar` - Cancelar matrícula

### Notas (`/v1/notas`)
- `POST /` - Lançar nota
- `GET /` - Listar notas
- `GET /{id}` - Obter nota
- `GET /matricula/{matricula_id}` - Notas de uma matrícula
- `PUT /{id}` - Corrigir nota
- `DELETE /{id}` - Deletar nota

### Relatórios (`/v1/relatorios`)
- `GET /boletim/{aluno_id}` - Boletim com notas e médias

### Status
- `GET /v1/health` - Health check

---

## 🏗️ Arquitetura em Camadas

```
┌─────────────────────────────────────────┐
│        FastAPI / HTTP Endpoints         │
├─────────────────────────────────────────┤
│    Router Layer (router/)               │
│    - Validação de entrada               │
│    - Serializadores Pydantic            │
├─────────────────────────────────────────┤
│    Service Layer (services/)            │
│    - Lógica de negócio                  │
│    - Validações complexas               │
│    - Orquestração                       │
├─────────────────────────────────────────┤
│    Domain Layer (domain/)               │
│    - Modelos SQLAlchemy                 │
│    - Entidades do negócio               │
├─────────────────────────────────────────┤
│    Database Layer (database/)           │
│    - Conexão SQLite                     │
│    - Transações                         │
└─────────────────────────────────────────┘
```

---

## 📊 Modelo de Dados

### Aluno
- `id`: int (PK)
- `nome`: string
- `email`: string (unique)
- `matricula`: string (unique)
- `periodo`: int (1-8)
- `data_criacao`: datetime

### Professor
- `id`: int (PK)
- `nome`: string
- `email`: string (unique)
- `especialidade`: string
- `data_criacao`: datetime

### Disciplina
- `id`: int (PK)
- `nome`: string
- `codigo`: string (unique)
- `carga_horaria`: int
- `professor_id`: int (FK)
- `data_criacao`: datetime

### Turma
- `id`: int (PK)
- `disciplina_id`: int (FK)
- `semestre`: int (1-2)
- `ano`: int
- `vagas`: int
- `data_criacao`: datetime

### Matrícula
- `id`: int (PK)
- `aluno_id`: int (FK)
- `turma_id`: int (FK)
- `data_matricula`: datetime
- `status`: enum (ativa | cancelada | concluída)
- `data_criacao`: datetime

### Nota
- `id`: int (PK)
- `matricula_id`: int (FK)
- `tipo`: enum (N1 | N2 | N3 | Final)
- `valor`: float (0-10)
- `data_lancamento`: datetime
- `data_criacao`: datetime

---

## 🗂️ Estrutura do Projeto

```
academico-api/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app
│   ├── domain/                      # Models SQLAlchemy
│   │   ├── __init__.py
│   │   └── models.py
│   ├── schemas/                     # Pydantic schemas
│   │   ├── __init__.py
│   │   └── schemas.py
│   ├── services/                    # Business logic
│   │   ├── __init__.py
│   │   ├── aluno_service.py
│   │   ├── professor_service.py
│   │   ├── disciplina_service.py
│   │   ├── matricula_service.py
│   │   ├── nota_service.py
│   │   └── relatorio_service.py
│   ├── router/                      # HTTP endpoints
│   │   ├── __init__.py
│   │   ├── aluno_router.py
│   │   ├── professor_router.py
│   │   ├── disciplina_router.py
│   │   ├── matricula_router.py
│   │   ├── nota_router.py
│   │   └── relatorio_router.py
│   └── database/                    # DB setup
│       ├── __init__.py
│       ├── connection.py
│       └── seed.py
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .gitignore
├── .dockerignore
├── FLUXOGRAMA.md
└── README.md
```

---

## 🧪 Testes

### Rodar Testes

```bash
# Todos os testes
pytest tests/ -v

# Com coverage
pytest tests/ --cov=app

# Arquivo específico
pytest tests/test_endpoints.py

# Função específica
pytest tests/test_endpoints.py::TestAlunos::test_criar_aluno -v
```

### Cobertura de Testes

- ✅ Endpoints de Alunos
- ✅ Endpoints de Professores
- ✅ Health check
- ✅ Validações Pydantic
- ✅ Erros 404, 400

---

## 🛠️ Desenvolvimento Local

### Pré-requisitos
- Python 3.11+
- pip ou uv

### Setup

```bash
# 1. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar servidor
uvicorn app.main:app --reload --port 8000
```

### Endpoints de teste
```bash
# Health check
curl http://localhost:8000/v1/health

# Docs
http://localhost:8000/docs
```

---

## 🐳 Docker

### Build manual

```bash
docker build -t academico-api .
```

### Executar manualmente

```bash
docker run -p 8000:8000 academico-api
```

### Com Docker Compose

```bash
docker-compose up
```

---

## 📝 Dados de Teste

A API vem com um seed automático ao iniciar:

| Recurso | Quantidade | Detalhes |
|---------|-----------|----------|
| Alunos | 5 | Inclui matrícula principal 2301045 |
| Professores | 3 | Com especialidades variadas |
| Disciplinas | 4 | Engenharia, BD, Algoritmos, ES2 |
| Matrículas | 11 | Alunos matriculados em várias disciplinas |
| Notas | 20+ | N1, N2, N3 para cada matrícula |

Acesse `/docs` para explorar via Swagger!

---

## 🏛️ Convençõesde Código

### Type Hints

```python
from typing import List, Optional
from sqlalchemy.orm import Session

def obter_alunos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
    """Listar alunos com paginação."""
    pass
```

### Docstrings

```python
def criar_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
    """
    Criar novo aluno.
    
    Args:
        db: Sessão do banco
        aluno: Dados do aluno
    
    Returns:
        Aluno criado com ID
    
    Raises:
        HTTPException: Se email duplicado
    """
    pass
```

Consulte [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md) para convenções completas.

---

## 📋 Requisitos Completados

✅ Arquitetura em camadas (domain, services, router, database)  
✅ Fluxograma em Mermaid (FLUXOGRAMA.md)  
✅ Seed com dados gerados por IA (5 alunos, 3 professores, 4 disciplinas)  
✅ Dockerfile e docker-compose  
✅ Endpoints CRUD completos  
✅ Endpoints de matrículas (criar, cancelar, consultar)  
✅ Endpoints de notas (lançar, corrigir, consultar)  
✅ Relatório de boletim  
✅ Health check com status do banco  
✅ Swagger em /docs  
✅ SQLite como banco de dados  
✅ Validação com Pydantic  
✅ Erro handling com HTTP status codes  
✅ Paginação em endpoints  
✅ README completo  

---

## 📞 Suporte

Para dúvidas ou issues, consulte:
- Documentação Swagger: http://localhost:8000/docs
- Fluxograma: Ver arquivo FLUXOGRAMA.md
- Exemplos: Ver seção "Exemplos de Uso" acima

---

## 📜 Licença

MIT

---

**Desenvolvido com ❤️ para fins acadêmicos**
