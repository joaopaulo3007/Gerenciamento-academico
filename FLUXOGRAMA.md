# Fluxograma da API Acadêmica

## Arquitetura em Camadas

```mermaid
graph TB
    Client["Cliente HTTP"]
    FastAPI["FastAPI Framework"]
    Router["Rotas - Router Layer"]
    Service["Serviços - Service Layer"]
    Domain["Domínio - Domain Models"]
    DB["Banco de Dados - SQLite"]
    
    Client -->|HTTP Request| FastAPI
    FastAPI --> Router
    Router -->|Chamadas| Service
    Service -->|Operações| Domain
    Domain -->|Queries/Commands| DB
    DB -->|Resposta| Domain
    Domain -->|Resultado| Service
    Service -->|Response| Router
    Router -->|JSON| FastAPI
    FastAPI -->|HTTP Response| Client
```

## Fluxo de Criação de Aluno

```mermaid
sequenceDiagram
    participant Cliente
    participant Router
    participant Service
    participant Database
    
    Cliente->>Router: POST /v1/alunos
    Router->>Service: criar_aluno()
    Service->>Service: Validar dados
    Service->>Database: INSERT INTO alunos
    Database-->>Service: Aluno criado com ID
    Service-->>Router: AlunoResponse
    Router-->>Cliente: 201 + JSON
```

## Fluxo de Matrícula e Consulta de Notas

```mermaid
graph LR
    subgraph "Aluno"
        A1["Aluno 1<br/>João Paulo Felisardo"]
    end
    
    subgraph "Matrículas"
        M1["Matrícula 1<br/>em Python"]
        M2["Matrícula 2<br/>em BD"]
    end
    
    subgraph "Notas"
        N1["N1: 8.5"]
        N2["N2: 9.0"]
        N3["N1: 7.5"]
        N4["N2: 8.0"]
    end
    
    A1 --> M1
    A1 --> M2
    M1 --> N1
    M1 --> N2
    M2 --> N3
    M2 --> N4
```

## Fluxo de Relatório (Boletim)

```mermaid
graph TD
    A["GET /v1/relatorios/boletim/{aluno_id}"]
    B["Buscar Aluno"]
    C["Buscar Matrículas Ativas"]
    D["Para cada Matrícula:<br/>- Buscar Turma<br/>- Buscar Disciplina<br/>- Buscar Professor"]
    E["Buscar Notas de cada Matrícula"]
    F["Calcular Média por Disciplina"]
    G["Calcular Média Geral"]
    H["Retornar BoletimResponse"]
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
```

## Estrutura de Diretórios

```
academico-api/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app + rotas globais
│   ├── domain/                      # Camada de Domínio
│   │   ├── __init__.py
│   │   └── models.py                # SQLAlchemy ORM Models
│   ├── schemas/                     # Camada de Esquemas
│   │   ├── __init__.py
│   │   └── schemas.py               # Pydantic schemas
│   ├── services/                    # Camada de Serviços (Business Logic)
│   │   ├── __init__.py
│   │   ├── aluno_service.py
│   │   ├── professor_service.py
│   │   ├── disciplina_service.py
│   │   ├── matricula_service.py
│   │   ├── nota_service.py
│   │   └── relatorio_service.py
│   ├── router/                      # Camada de Rotas (HTTP Endpoints)
│   │   ├── __init__.py
│   │   ├── aluno_router.py
│   │   ├── professor_router.py
│   │   ├── disciplina_router.py
│   │   ├── matricula_router.py
│   │   ├── nota_router.py
│   │   └── relatorio_router.py
│   └── database/                    # Camada de Banco de Dados
│       ├── __init__.py
│       ├── connection.py            # SQLAlchemy setup
│       └── seed.py                  # Seed com dados de exemplo
├── Dockerfile                       # Configuração do container
├── docker-compose.yml               # Orquestração de containers
├── requirements.txt                 # Dependências Python
├── pyproject.toml                   # Configuração do projeto
├── .gitignore
├── .dockerignore
├── README.md
└── FLUXOGRAMA.md
```

## Endpoints Principais

```mermaid
graph LR
    API["API /v1"]
    
    API -->|CRUD| AL["Alunos"]
    API -->|CRUD| PR["Professores"]
    API -->|CRUD| DI["Disciplinas"]
    API -->|Criar/Cancelar| MA["Matrículas"]
    API -->|Lançar/Corrigir| NO["Notas"]
    API -->|Consultar| RE["Relatórios"]
    API -->|Status| HE["Health"]
    
    AL -.-> EP1["GET /alunos<br/>POST /alunos<br/>GET /alunos/{id}<br/>PUT /alunos/{id}<br/>DELETE /alunos/{id}"]
    MA -.-> EP2["POST /matriculas<br/>GET /matriculas<br/>POST /matriculas/{id}/cancelar"]
    NO -.-> EP3["POST /notas<br/>GET /notas<br/>PUT /notas/{id}"]
    RE -.-> EP4["GET /relatorios/boletim/{aluno_id}"]
```

## Entidades e Relacionamentos

```mermaid
erDiagram
    ALUNO ||--o{ MATRICULA : tem
    PROFESSOR ||--o{ DISCIPLINA : leciona
    DISCIPLINA ||--o{ TURMA : oferece
    TURMA ||--o{ MATRICULA : possui
    MATRICULA ||--o{ NOTA : contains
    
    ALUNO {
        int id
        string nome
        string email
        string matricula
        int periodo
        datetime data_criacao
    }
    
    PROFESSOR {
        int id
        string nome
        string email
        string especialidade
        datetime data_criacao
    }
    
    DISCIPLINA {
        int id
        string nome
        string codigo
        int carga_horaria
        int professor_id
        datetime data_criacao
    }
    
    TURMA {
        int id
        int disciplina_id
        int semestre
        int ano
        int vagas
        datetime data_criacao
    }
    
    MATRICULA {
        int id
        int aluno_id
        int turma_id
        datetime data_matricula
        enum status
        datetime data_criacao
    }
    
    NOTA {
        int id
        int matricula_id
        enum tipo
        float valor
        datetime data_lancamento
        datetime data_criacao
    }
```

## Fluxo de Deploy com Docker

```mermaid
graph TB
    A["docker-compose up --build"]
    B["Construir Imagem Docker"]
    C["Instalar Dependências"]
    D["Copiar Código"]
    E["Iniciar Container"]
    F["Criar Banco de Dados"]
    G["Popular com Seed"]
    H["Uvicorn Startup"]
    I["API Pronta em :8000"]
    J["Swagger em /docs"]
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    F --> G
    G --> H
    H --> I
    H --> J
```
