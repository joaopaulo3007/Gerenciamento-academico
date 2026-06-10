from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BoletimResponse
from app.services import RelatorioService

router = APIRouter(prefix="/v1/relatorios", tags=["Relatórios"])


@router.get("/boletim/{aluno_id}", response_model=BoletimResponse)
def gerar_boletim(aluno_id: int, db: Session = Depends(get_db)):
    """Gerar boletim do aluno com notas e média por disciplina"""
    return RelatorioService.gerar_boletim(db, aluno_id)
