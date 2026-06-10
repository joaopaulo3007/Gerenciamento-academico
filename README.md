# 🎓 API de Gerenciamento Acadêmico

Uma API REST completa para gerenciar sistemas acadêmicos com cadastro de alunos, professores, disciplinas, turmas, matrículas e notas.

**Stack**: FastAPI + SQLite + Docker  
**Arquitetura**: Camadas (Domain, Services, Router, Database)

---

## 📋 Características

✅ **CRUD Completo** para Alunos e Disciplinas  
✅ **Gestão de Matrículas** - criar, cancelar, consultar  
✅ **Gestão de Notas** - lançar, corrigir, consultar  
✅ **Relatórios** - boletim do aluno com médias por disciplina  
✅ **Health Check** - status da API e conexão com banco  
✅ **Swagger/OpenAPI** - documentação automática em `/docs`  
✅ **Seed de Dados** - 5 alunos, 3 professores, 4 disciplinas com notas  
✅ **Docker** - Dockerfile e docker-compose inclusos  
✅ **Validação** - schemas Pydantic com validação automática  

---

## 🚀 Quick Start com Docker

### Pré-requisitos
- Docker e Docker Compose instalados
- Git (opcional, para clonar)

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
    "nome": "João Silva",
    "email": "joao@example.com",
    "matricula": "2024001",
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

## 🛠️ Desenvolvimento Local (sem Docker)

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

**Alunos**: 5 alunos com matrículas
**Professores**: 3 professores
**Disciplinas**: 4 disciplinas
**Matrículas**: 11 registros
**Notas**: Múltiplas notas (N1, N2, N3) para cada matrícula

Acesse `/docs` para explorar via Swagger!

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
