from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import NotaCreate, NotaUpdate, NotaResponse
from app.services import NotaService

router = APIRouter(prefix="/v1/notas", tags=["Notas"])


@router.post("/", response_model=NotaResponse, status_code=status.HTTP_201_CREATED)
def lançar_nota(nota: NotaCreate, db: Session = Depends(get_db)):
    """Lançar nova nota"""
    return NotaService.lançar_nota(db, nota)


@router.get("/", response_model=list[NotaResponse])
def listar_notas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Listar todas as notas"""
    return NotaService.obter_notas(db, skip, limit)


@router.get("/{nota_id}", response_model=NotaResponse)
def obter_nota(nota_id: int, db: Session = Depends(get_db)):
    """Obter nota por ID"""
    return NotaService.obter_nota_por_id(db, nota_id)


@router.get("/matricula/{matricula_id}", response_model=list[NotaResponse])
def listar_notas_matricula(matricula_id: int, db: Session = Depends(get_db)):
    """Listar notas de uma matrícula"""
    return NotaService.obter_notas_por_matricula(db, matricula_id)


@router.put("/{nota_id}", response_model=NotaResponse)
def corrigir_nota(nota_id: int, nota: NotaUpdate, db: Session = Depends(get_db)):
    """Corrigir nota"""
    return NotaService.corrigir_nota(db, nota_id, nota)


@router.delete("/{nota_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_nota(nota_id: int, db: Session = Depends(get_db)):
    """Deletar nota"""
    NotaService.deletar_nota(db, nota_id)
