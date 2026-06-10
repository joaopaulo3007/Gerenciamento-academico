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

app = FastAPI(
    title="Sistema Acadêmico",
    description="API REST de gerenciamento acadêmico",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar banco de dados na startup
@app.on_event("startup")
def startup_event():
    init_db()
    db = next(get_db())
    try:
        seed_database(db)
    finally:
        db.close()


# Rotas
app.include_router(aluno_router)
app.include_router(professor_router)
app.include_router(disciplina_router)
app.include_router(matricula_router)
app.include_router(nota_router)
app.include_router(relatorio_router)


@app.get("/")
def root():
    """Endpoint raiz da API"""
    return {
        "mensagem": "API Acadêmica funcionando",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/v1/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health check com status da API e conexão com banco"""
    try:
        # Testar conexão com banco
        db.execute("SELECT 1")
        database_status = "connected"
    except Exception as e:
        database_status = f"disconnected: {str(e)}"
    
    return HealthResponse(
        status="online",
        database=database_status,
        version="1.0.0",
        timestamp=datetime.utcnow()
    )