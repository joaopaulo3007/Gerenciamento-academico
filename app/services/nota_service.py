from sqlalchemy.orm import Session
from app.domain.models import Nota, Matricula, TipoNota
from app.schemas import NotaCreate, NotaUpdate
from typing import List, Optional
from fastapi import HTTPException, status


class NotaService:
    @staticmethod
    def lançar_nota(db: Session, nota: NotaCreate) -> Nota:
        """Lançar nova nota"""
        # Verificar se matrícula existe
        matricula = db.query(Matricula).filter(Matricula.id == nota.matricula_id).first()
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matrícula não encontrada"
            )
        
        # Verificar se já existe nota do mesmo tipo
        existente = db.query(Nota).filter(
            Nota.matricula_id == nota.matricula_id,
            Nota.tipo == nota.tipo
        ).first()
        
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Nota {nota.tipo} já lançada para esta matrícula"
            )
        
        db_nota = Nota(**nota.dict())
        db.add(db_nota)
        db.commit()
        db.refresh(db_nota)
        return db_nota

    @staticmethod
    def obter_notas(db: Session, skip: int = 0, limit: int = 100) -> List[Nota]:
        """Listar todas as notas"""
        return db.query(Nota).offset(skip).limit(limit).all()

    @staticmethod
    def obter_nota_por_id(db: Session, nota_id: int) -> Optional[Nota]:
        """Obter nota por ID"""
        nota = db.query(Nota).filter(Nota.id == nota_id).first()
        if not nota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nota não encontrada"
            )
        return nota

    @staticmethod
    def obter_notas_por_matricula(db: Session, matricula_id: int) -> List[Nota]:
        """Obter todas as notas de uma matrícula"""
        return db.query(Nota).filter(Nota.matricula_id == matricula_id).all()

    @staticmethod
    def corrigir_nota(db: Session, nota_id: int, nota_update: NotaUpdate) -> Nota:
        """Corrigir valor da nota"""
        db_nota = NotaService.obter_nota_por_id(db, nota_id)
        db_nota.valor = nota_update.valor
        db.commit()
        db.refresh(db_nota)
        return db_nota

    @staticmethod
    def deletar_nota(db: Session, nota_id: int):
        """Deletar nota"""
        db_nota = NotaService.obter_nota_por_id(db, nota_id)
        db.delete(db_nota)
        db.commit()

    @staticmethod
    def calcular_media(db: Session, matricula_id: int) -> float:
        """Calcular média de uma matrícula"""
        notas = db.query(Nota).filter(Nota.matricula_id == matricula_id).all()
        
        if not notas:
            return 0.0
        
        return sum(n.valor for n in notas) / len(notas)
