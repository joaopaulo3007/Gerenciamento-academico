from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse
from app.services import DisciplinaService

router = APIRouter(prefix="/v1/disciplinas", tags=["Disciplinas"])


@router.post("/", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED)
def criar_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    """Criar nova disciplina"""
    return DisciplinaService.criar_disciplina(db, disciplina)


@router.get("/", response_model=list[DisciplinaResponse])
def listar_disciplinas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as disciplinas"""
    return DisciplinaService.obter_disciplinas(db, skip, limit)


@router.get("/{disciplina_id}", response_model=DisciplinaResponse)
def obter_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    """Obter disciplina por ID"""
    return DisciplinaService.obter_disciplina_por_id(db, disciplina_id)


@router.put("/{disciplina_id}", response_model=DisciplinaResponse)
def atualizar_disciplina(disciplina_id: int, disciplina: DisciplinaUpdate, db: Session = Depends(get_db)):
    """Atualizar disciplina"""
    return DisciplinaService.atualizar_disciplina(db, disciplina_id, disciplina)


@router.delete("/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_disciplina(disciplina_id: int, db: Session = Depends(get_db)):
    """Deletar disciplina"""
    DisciplinaService.deletar_disciplina(db, disciplina_id)
