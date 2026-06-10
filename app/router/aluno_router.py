from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AlunoCreate, AlunoUpdate, AlunoResponse
from app.services import AlunoService

router = APIRouter(prefix="/v1/alunos", tags=["Alunos"])


@router.post("/", response_model=AlunoResponse, status_code=status.HTTP_201_CREATED)
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    """Criar novo aluno"""
    return AlunoService.criar_aluno(db, aluno)


@router.get("/", response_model=list[AlunoResponse])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os alunos com paginação"""
    return AlunoService.obter_alunos(db, skip, limit)


@router.get("/{aluno_id}", response_model=AlunoResponse)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Obter aluno por ID"""
    return AlunoService.obter_aluno_por_id(db, aluno_id)


@router.put("/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(aluno_id: int, aluno: AlunoUpdate, db: Session = Depends(get_db)):
    """Atualizar aluno"""
    return AlunoService.atualizar_aluno(db, aluno_id, aluno)


@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Deletar aluno"""
    AlunoService.deletar_aluno(db, aluno_id)
