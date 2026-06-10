# 🔒 Segurança e Configuração

Guia de boas práticas de segurança para o projeto.

---

## 📋 Índice

- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [CORS](#cors)
- [Validação de Entrada](#validação-de-entrada)
- [Tratamento de Erros](#tratamento-de-erros)
- [Logging Seguro](#logging-seguro)
- [SQL Injection Prevention](#sql-injection-prevention)
- [Secrets Management](#secrets-management)

---

## Variáveis de Ambiente

### Configuração

Arquivo `.env.example`:

```env
# Database
DATABASE_URL=sqlite:///./academic.db

# Debug
DEBUG=False

# API
API_TITLE=Sistema Acadêmico API
API_VERSION=1.0.0

# Security
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
```

### Uso no Código

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    database_url: str = "sqlite:///./academic.db"
    debug: bool = False
    api_title: str = "Sistema Acadêmico API"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## CORS

### Configuração Segura

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Em produção, especificar
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Em Desenvolvimento vs Produção

```python
import os

if os.getenv("DEBUG"):
    # Desenvolvimento
    allow_origins = ["*"]
else:
    # Produção
    allow_origins = ["https://seu-dominio.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    # ...
)
```

---

## Validação de Entrada

### Usar Pydantic para Validar

```python
from pydantic import BaseModel, EmailStr, Field

class AlunoCreate(BaseModel):
    """Schema para criar aluno com validações."""
    
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr  # Valida automaticamente email
    matricula: str = Field(..., min_length=5, max_length=20)
    periodo: int = Field(..., ge=1, le=8)  # Entre 1 e 8
```

### Validações Customizadas

```python
from pydantic import validator

class AlunoCreate(BaseModel):
    nome: str
    email: str
    
    @validator('email')
    def email_deve_ser_institucional(cls, v):
        if not v.endswith('@academico.com'):
            raise ValueError('Email deve ser institucional')
        return v.lower()
    
    @validator('nome')
    def nome_nao_pode_conter_numeros(cls, v):
        if any(char.isdigit() for char in v):
            raise ValueError('Nome não pode conter números')
        return v
```

---

## Tratamento de Erros

### Nunca Expor Detalhes Internos

```python
# ❌ ERRADO - Expõe informações do banco
try:
    db.query(Aluno).add(aluno)
except Exception as e:
    raise HTTPException(
        status_code=500,
        detail=str(e)  # Expõe erro interno!
    )

# ✅ CORRETO - Mensagem genérica
try:
    db.query(Aluno).add(aluno)
except Exception as e:
    logger.error(f"Erro ao criar aluno: {e}")
    raise HTTPException(
        status_code=500,
        detail="Erro ao processar solicitação"
    )
```

### Error Handler Customizado

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Tratador genérico de exceções."""
    logger.error(f"Erro não tratado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro ao processar solicitação"}
    )
```

---

## Logging Seguro

### Não Logar Dados Sensíveis

```python
# ❌ ERRADO - Loga senha
logger.info(f"Login: {user.email}, {password}")

# ✅ CORRETO - Sem dados sensíveis
logger.info(f"Login attempt para {user.email}")

# ❌ ERRADO - Loga dados completos
logger.debug(f"Dados do aluno: {aluno.dict()}")

# ✅ CORRETO - Apenas ID
logger.debug(f"Processando aluno ID {aluno.id}")
```

### Mascarar Informações Sensíveis

```python
def mascarar_email(email: str) -> str:
    """Mascarar email para logging."""
    nome, dominio = email.split('@')
    return f"{nome[0]}***@{dominio}"

logger.info(f"Email verificado: {mascarar_email(user.email)}")
```

---

## SQL Injection Prevention

### Usar SQLAlchemy ORM (Seguro)

```python
# ✅ SEGURO - Usa parameterized queries
aluno = db.query(Aluno).filter(Aluno.email == email).first()

# ❌ NUNCA - String interpolation
aluno = db.execute(f"SELECT * FROM alunos WHERE email = '{email}'")
```

### Validar Entrada

```python
from pydantic import validator

class EmailSearch(BaseModel):
    email: str
    
    @validator('email')
    def validar_email(cls, v):
        if not isinstance(v, str) or len(v) > 100:
            raise ValueError('Email inválido')
        return v.lower()
```

---

## Secrets Management

### Em Desenvolvimento

```bash
# Criar .env (NÃO commitar!)
echo ".env" >> .gitignore

# Conteúdo de .env
SECRET_KEY=minha-chave-secreta-desenvolvimento
DATABASE_URL=sqlite:///./academic.db
DEBUG=True
```

### Em Produção

```bash
# Usar variáveis de ambiente do sistema
export SECRET_KEY="chave-produção-super-secreta"
export DEBUG=False
export DATABASE_URL="postgresql://user:pass@prod-db:5432/academico"

# Ou usar gestor de secrets
# - AWS Secrets Manager
# - HashiCorp Vault
# - Azure Key Vault
```

### Arquivo de Configuração

```python
# config.py
import os
from functools import lru_cache

class Settings:
    """Configurações da aplicação."""
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-key-change-in-production")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./academic.db")
    
    @property
    def database_params(self):
        """Parâmetros seguros do banco."""
        if self.DATABASE_URL.startswith("sqlite"):
            return {"check_same_thread": False}
        return {}

@lru_cache()
def get_settings() -> Settings:
    """Obter configurações em cache."""
    return Settings()
```

---

## Rate Limiting (Futuro)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/v1/alunos")
@limiter.limit("100/minute")
def listar_alunos(request: Request):
    """Máximo 100 requisições por minuto."""
    pass
```

---

## Checklist de Segurança

- [ ] Usar HTTPS em produção
- [ ] Validar todas as entradas
- [ ] Nunca logar senhas ou tokens
- [ ] Usar SQLAlchemy ORM
- [ ] Implementar rate limiting
- [ ] CORS configurado corretamente
- [ ] Secrets em variáveis de ambiente
- [ ] Mensagens de erro genéricas
- [ ] SQL parametrizado (ORM)
- [ ] Headers de segurança

---

**Segurança é responsabilidade de todos! 🔒**
