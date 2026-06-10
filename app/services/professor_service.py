from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.models import Professor
from app.schemas import ProfessorCreate, ProfessorUpdate
from typing import List, Optional
from fastapi import HTTPException, status


class ProfessorService:
    @staticmethod
    def criar_professor(db: Session, professor: ProfessorCreate) -> Professor:
        """Criar novo professor"""
        try:
            db_professor = Professor(**professor.dict())
            db.add(db_professor)
            db.commit()
            db.refresh(db_professor)
            return db_professor
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

    @staticmethod
    def obter_professores(db: Session, skip: int = 0, limit: int = 100) -> List[Professor]:
        """Listar todos os professores"""
        return db.query(Professor).offset(skip).limit(limit).all()

    @staticmethod
    def obter_professor_por_id(db: Session, professor_id: int) -> Optional[Professor]:
        """Obter professor por ID"""
        professor = db.query(Professor).filter(Professor.id == professor_id).first()
        if not professor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Professor não encontrado"
            )
        return professor

    @staticmethod
    def atualizar_professor(db: Session, professor_id: int, professor_update: ProfessorUpdate) -> Professor:
        """Atualizar professor"""
        db_professor = ProfessorService.obter_professor_por_id(db, professor_id)
        
        dados_atualizacao = professor_update.dict(exclude_unset=True)
        for campo, valor in dados_atualizacao.items():
            setattr(db_professor, campo, valor)
        
        try:
            db.commit()
            db.refresh(db_professor)
            return db_professor
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

    @staticmethod
    def deletar_professor(db: Session, professor_id: int):
        """Deletar professor"""
        db_professor = ProfessorService.obter_professor_por_id(db, professor_id)
        db.delete(db_professor)
        db.commit()
