"""
API de Gerenciamento Acadêmico - Aplicação Principal

Módulo responsável pela configuração e inicialização da aplicação FastAPI.
Define middlewares, event handlers e endpoints globais.

Author: Sistema Acadêmico
Version: 1.0.0
"""

import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy.orm import Session

from app.database import init_db, seed_database, get_db
from app.schemas import HealthResponse
from app.router import (
    aluno_router,
    professor_router,
    disciplina_router,
    matricula_router,
    nota_router,
    relatorio_router,
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Criar instância FastAPI
app = FastAPI(
    title="Sistema Acadêmico API",
    description="API REST para gerenciamento acadêmico com FastAPI + SQLite",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Suporte",
        "url": "https://github.com/academico-api",
    },
    license_info={
        "name": "MIT",
    },
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event: Startup - Inicializar banco de dados
@app.on_event("startup")
def startup_event() -> None:
    """
    Event handler executado ao iniciar a aplicação.
    
    Responsabilidades:
    - Criar tabelas do banco de dados
    - Popular banco com dados de exemplo (seed)
    - Validar conexão com banco
    """
    logger.info("🚀 Iniciando aplicação...")
    
    try:
        init_db()
        logger.info("✓ Banco de dados inicializado")
        
        db = next(get_db())
        try:
            seed_database(db)
            logger.info("✓ Seed de dados populado")
        finally:
            db.close()
        
        logger.info("✓ Aplicação pronta!")
    except Exception as e:
        logger.error(f"✗ Erro ao iniciar aplicação: {e}")
        raise


# Incluir routers
app.include_router(aluno_router)
app.include_router(professor_router)
app.include_router(disciplina_router)
app.include_router(matricula_router)
app.include_router(nota_router)
app.include_router(relatorio_router)


@app.get("/", tags=["Root"])
def root() -> dict:
    """
    Endpoint raiz da API.
    
    Retorna informações básicas sobre a API.
    
    Returns:
        dict: Informações da API (versão, URLs de documentação)
    """
    return {
        "mensagem": "API de Gerenciamento Acadêmico",
        "version": "1.0.0",
        "ambiente": "produção",
        "docs": {
            "swagger": "/docs",
            "redoc": "/redoc",
        }
    }


@app.get("/v1/health", response_model=HealthResponse, tags=["Health"])
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """
    Health check da API com status da conexão com banco de dados.
    
    Verifica:
    - Status da API
    - Conexão com o banco SQLite
    - Versão da aplicação
    
    Args:
        db: Sessão do banco de dados
    
    Returns:
        HealthResponse: Status da API e banco de dados
    
    Raises:
        HTTPException: Se houver erro na conexão
    """
    database_status = "connected"
    
    try:
        db.execute("SELECT 1")
        logger.debug("✓ Conexão com banco validada")
    except Exception as e:
        database_status = f"disconnected"
        logger.error(f"✗ Erro na conexão com banco: {e}")
    
    return HealthResponse(
        status="online",
        database=database_status,
        version="1.0.0",
        timestamp=datetime.utcnow()
    )