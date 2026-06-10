from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.domain.models import Aluno
from app.schemas import AlunoCreate, AlunoUpdate
from typing import List, Optional
from fastapi import HTTPException, status


class AlunoService:
    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
        """Criar novo aluno"""
        try:
            db_aluno = Aluno(**aluno.dict())
            db.add(db_aluno)
            db.commit()
            db.refresh(db_aluno)
            return db_aluno
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ou matrícula já cadastrados"
            )

    @staticmethod
    def obter_alunos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """Listar todos os alunos com paginação"""
        return db.query(Aluno).offset(skip).limit(limit).all()

    @staticmethod
    def obter_aluno_por_id(db: Session, aluno_id: int) -> Optional[Aluno]:
        """Obter aluno por ID"""
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return aluno

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str) -> Optional[Aluno]:
        """Obter aluno por email"""
        return db.query(Aluno).filter(Aluno.email == email).first()

    @staticmethod
    def obter_aluno_por_matricula(db: Session, matricula: str) -> Optional[Aluno]:
        """Obter aluno por matrícula"""
        aluno = db.query(Aluno).filter(Aluno.matricula == matricula).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return aluno

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, aluno_update: AlunoUpdate) -> Aluno:
        """Atualizar aluno"""
        db_aluno = AlunoService.obter_aluno_por_id(db, aluno_id)
        
        dados_atualizacao = aluno_update.dict(exclude_unset=True)
        for campo, valor in dados_atualizacao.items():
            setattr(db_aluno, campo, valor)
        
        try:
            db.commit()
            db.refresh(db_aluno)
            return db_aluno
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int):
        """Deletar aluno"""
        db_aluno = AlunoService.obter_aluno_por_id(db, aluno_id)
        db.delete(db_aluno)
        db.commit()
