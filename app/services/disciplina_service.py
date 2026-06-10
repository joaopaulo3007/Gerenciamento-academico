from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.models import Disciplina, Professor
from app.schemas import DisciplinaCreate, DisciplinaUpdate
from typing import List, Optional
from fastapi import HTTPException, status


class DisciplinaService:
    @staticmethod
    def criar_disciplina(db: Session, disciplina: DisciplinaCreate) -> Disciplina:
        """Criar nova disciplina"""
        # Verificar se professor existe
        professor = db.query(Professor).filter(Professor.id == disciplina.professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )
        
        try:
            db_disciplina = Disciplina(**disciplina.dict())
            db.add(db_disciplina)
            db.commit()
            db.refresh(db_disciplina)
            return db_disciplina
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Código de disciplina já cadastrado"
            )

    @staticmethod
    def obter_disciplinas(db: Session, skip: int = 0, limit: int = 100) -> List[Disciplina]:
        """Listar todas as disciplinas"""
        return db.query(Disciplina).offset(skip).limit(limit).all()

    @staticmethod
    def obter_disciplina_por_id(db: Session, disciplina_id: int) -> Optional[Disciplina]:
        """Obter disciplina por ID"""
        disciplina = db.query(Disciplina).filter(Disciplina.id == disciplina_id).first()
        if not disciplina:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Disciplina não encontrada"
            )
        return disciplina

    @staticmethod
    def atualizar_disciplina(db: Session, disciplina_id: int, disciplina_update: DisciplinaUpdate) -> Disciplina:
        """Atualizar disciplina"""
        db_disciplina = DisciplinaService.obter_disciplina_por_id(db, disciplina_id)
        
        dados_atualizacao = disciplina_update.dict(exclude_unset=True)
        
        # Se está alterando professor, verificar se existe
        if "professor_id" in dados_atualizacao:
            professor = db.query(Professor).filter(Professor.id == dados_atualizacao["professor_id"]).first()
            if not professor:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Professor não encontrado"
                )
        
        for campo, valor in dados_atualizacao.items():
            setattr(db_disciplina, campo, valor)
        
        db.commit()
        db.refresh(db_disciplina)
        return db_disciplina

    @staticmethod
    def deletar_disciplina(db: Session, disciplina_id: int):
        """Deletar disciplina"""
        db_disciplina = DisciplinaService.obter_disciplina_por_id(db, disciplina_id)
        db.delete(db_disciplina)
        db.commit()
