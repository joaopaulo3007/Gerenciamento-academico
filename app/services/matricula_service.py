from sqlalchemy.orm import Session
from app.domain.models import Matricula, Turma, Aluno, Nota, TipoNota, StatusMatricula
from app.schemas import MatriculaCreate, MatriculaUpdate
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy import func


class MatriculaService:
    @staticmethod
    def criar_matricula(db: Session, matricula: MatriculaCreate) -> Matricula:
        """Criar nova matrícula"""
        # Verificar se aluno existe
        aluno = db.query(Aluno).filter(Aluno.id == matricula.aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        
        # Verificar se turma existe
        turma = db.query(Turma).filter(Turma.id == matricula.turma_id).first()
        if not turma:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Turma não encontrada"
            )
        
        # Verificar se já existe matrícula ativa
        existente = db.query(Matricula).filter(
            Matricula.aluno_id == matricula.aluno_id,
            Matricula.turma_id == matricula.turma_id,
            Matricula.status == StatusMatricula.ATIVA
        ).first()
        
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aluno já está matriculado nesta turma"
            )
        
        # Verificar disponibilidade de vagas
        matriculados = db.query(func.count(Matricula.id)).filter(
            Matricula.turma_id == matricula.turma_id,
            Matricula.status == StatusMatricula.ATIVA
        ).scalar()
        
        if matriculados >= turma.vagas:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Turma sem vagas disponíveis"
            )
        
        db_matricula = Matricula(**matricula.dict(), status=StatusMatricula.ATIVA)
        db.add(db_matricula)
        db.commit()
        db.refresh(db_matricula)
        return db_matricula

    @staticmethod
    def obter_matriculas(db: Session, skip: int = 0, limit: int = 100) -> List[Matricula]:
        """Listar todas as matrículas"""
        return db.query(Matricula).offset(skip).limit(limit).all()

    @staticmethod
    def obter_matricula_por_id(db: Session, matricula_id: int) -> Optional[Matricula]:
        """Obter matrícula por ID"""
        matricula = db.query(Matricula).filter(Matricula.id == matricula_id).first()
        if not matricula:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Matrícula não encontrada"
            )
        return matricula

    @staticmethod
    def obter_matriculas_por_aluno(db: Session, aluno_id: int) -> List[Matricula]:
        """Obter matrículas de um aluno"""
        return db.query(Matricula).filter(Matricula.aluno_id == aluno_id).all()

    @staticmethod
    def obter_matriculas_por_turma(db: Session, turma_id: int) -> List[Matricula]:
        """Obter matrículas de uma turma"""
        return db.query(Matricula).filter(Matricula.turma_id == turma_id).all()

    @staticmethod
    def cancelar_matricula(db: Session, matricula_id: int) -> Matricula:
        """Cancelar matrícula"""
        db_matricula = MatriculaService.obter_matricula_por_id(db, matricula_id)
        
        if db_matricula.status == StatusMatricula.CANCELADA:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Matrícula já está cancelada"
            )
        
        db_matricula.status = StatusMatricula.CANCELADA
        db.commit()
        db.refresh(db_matricula)
        return db_matricula

    @staticmethod
    def atualizar_status_matricula(db: Session, matricula_id: int, matricula_update: MatriculaUpdate) -> Matricula:
        """Atualizar status da matrícula"""
        db_matricula = MatriculaService.obter_matricula_por_id(db, matricula_id)
        
        if matricula_update.status:
            db_matricula.status = matricula_update.status
        
        db.commit()
        db.refresh(db_matricula)
        return db_matricula

    @staticmethod
    def consultar_matricula(db: Session, aluno_id: int, turma_id: int) -> Optional[Matricula]:
        """Consultar matrícula específica"""
        return db.query(Matricula).filter(
            Matricula.aluno_id == aluno_id,
            Matricula.turma_id == turma_id
        ).first()
