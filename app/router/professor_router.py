from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ProfessorCreate, ProfessorUpdate, ProfessorResponse
from app.services import ProfessorService

router = APIRouter(prefix="/v1/professores", tags=["Professores"])


@router.post("/", response_model=ProfessorResponse, status_code=status.HTTP_201_CREATED)
def criar_professor(professor: ProfessorCreate, db: Session = Depends(get_db)):
    """Criar novo professor"""
    return ProfessorService.criar_professor(db, professor)


@router.get("/", response_model=list[ProfessorResponse])
def listar_professores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todos os professores"""
    return ProfessorService.obter_professores(db, skip, limit)


@router.get("/{professor_id}", response_model=ProfessorResponse)
def obter_professor(professor_id: int, db: Session = Depends(get_db)):
    """Obter professor por ID"""
    return ProfessorService.obter_professor_por_id(db, professor_id)


@router.put("/{professor_id}", response_model=ProfessorResponse)
def atualizar_professor(professor_id: int, professor: ProfessorUpdate, db: Session = Depends(get_db)):
    """Atualizar professor"""
    return ProfessorService.atualizar_professor(db, professor_id, professor)


@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_professor(professor_id: int, db: Session = Depends(get_db)):
    """Deletar professor"""
    ProfessorService.deletar_professor(db, professor_id)
