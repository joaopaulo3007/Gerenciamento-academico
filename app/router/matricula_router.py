from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MatriculaCreate, MatriculaUpdate, MatriculaResponse
from app.services import MatriculaService

router = APIRouter(prefix="/v1/matriculas", tags=["Matrículas"])


@router.post("/", response_model=MatriculaResponse, status_code=status.HTTP_201_CREATED)
def criar_matricula(matricula: MatriculaCreate, db: Session = Depends(get_db)):
    """Criar nova matrícula"""
    return MatriculaService.criar_matricula(db, matricula)


@router.get("/", response_model=list[MatriculaResponse])
def listar_matriculas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as matrículas"""
    return MatriculaService.obter_matriculas(db, skip, limit)


@router.get("/{matricula_id}", response_model=MatriculaResponse)
def obter_matricula(matricula_id: int, db: Session = Depends(get_db)):
    """Obter matrícula por ID"""
    return MatriculaService.obter_matricula_por_id(db, matricula_id)


@router.get("/aluno/{aluno_id}", response_model=list[MatriculaResponse])
def listar_matriculas_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Listar matrículas de um aluno"""
    return MatriculaService.obter_matriculas_por_aluno(db, aluno_id)


@router.post("/{matricula_id}/cancelar", response_model=MatriculaResponse)
def cancelar_matricula(matricula_id: int, db: Session = Depends(get_db)):
    """Cancelar matrícula"""
    return MatriculaService.cancelar_matricula(db, matricula_id)


@router.put("/{matricula_id}", response_model=MatriculaResponse)
def atualizar_matricula(matricula_id: int, matricula: MatriculaUpdate, db: Session = Depends(get_db)):
    """Atualizar status da matrícula"""
    return MatriculaService.atualizar_status_matricula(db, matricula_id, matricula)
