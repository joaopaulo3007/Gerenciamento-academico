"""
Serviço de Alunos - Lógica de Negócio

Responsável por operações CRUD e validações de alunos.
Implementa regras de negócio específicas do domínio.

Author: Sistema Acadêmico
Version: 1.0.0
"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.domain.models import Aluno
from app.schemas import AlunoCreate, AlunoUpdate

logger = logging.getLogger(__name__)


class AlunoService:
    """
    Serviço para gerenciar operações relacionadas a Alunos.
    
    Métodos:
    - criar_aluno: Criar novo aluno
    - obter_alunos: Listar alunos com paginação
    - obter_aluno_por_id: Buscar aluno por ID
    - obter_aluno_por_email: Buscar aluno por email
    - obter_aluno_por_matricula: Buscar aluno por matrícula
    - atualizar_aluno: Atualizar dados do aluno
    - deletar_aluno: Remover aluno
    """

    @staticmethod
    def criar_aluno(db: Session, aluno: AlunoCreate) -> Aluno:
        """
        Criar novo aluno no banco de dados.
        
        Args:
            db: Sessão do banco de dados
            aluno: Dados do aluno a criar (AlunoCreate)
        
        Returns:
            Aluno: Objeto aluno criado com ID gerado
        
        Raises:
            HTTPException: Se email ou matrícula já existem (400)
        
        Example:
            >>> aluno_data = AlunoCreate(
            ...     nome="João Paulo Felisardo",
            ...     email="joaopaulodemoraesfelisardo@gmail.com",
            ...     matricula="2301045",
            ...     periodo=1
            ... )
            >>> aluno = AlunoService.criar_aluno(db, aluno_data)
        """
        try:
            db_aluno = Aluno(**aluno.dict())
            db.add(db_aluno)
            db.commit()
            db.refresh(db_aluno)
            logger.info(f"✓ Aluno criado: {db_aluno.nome} ({db_aluno.matricula})")
            return db_aluno
        except IntegrityError as e:
            db.rollback()
            logger.error(f"✗ Erro ao criar aluno: Email ou matrícula duplicada")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ou matrícula já cadastrados"
            )

    @staticmethod
    def obter_alunos(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
        """
        Listar todos os alunos com paginação.
        
        Args:
            db: Sessão do banco de dados
            skip: Número de registros a pular (padrão: 0)
            limit: Número máximo de registros a retornar (padrão: 100)
        
        Returns:
            List[Aluno]: Lista de alunos
        
        Example:
            >>> alunos = AlunoService.obter_alunos(db, skip=0, limit=10)
            >>> print(f"Retornados {len(alunos)} alunos")
        """
        return db.query(Aluno).offset(skip).limit(limit).all()

    @staticmethod
    def obter_aluno_por_id(db: Session, aluno_id: int) -> Aluno:
        """
        Obter aluno específico por ID.
        
        Args:
            db: Sessão do banco de dados
            aluno_id: ID do aluno
        
        Returns:
            Aluno: Objeto aluno encontrado
        
        Raises:
            HTTPException: Se aluno não encontrado (404)
        
        Example:
            >>> aluno = AlunoService.obter_aluno_por_id(db, aluno_id=1)
        """
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            logger.warning(f"✗ Aluno com ID {aluno_id} não encontrado")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return aluno

    @staticmethod
    def obter_aluno_por_email(db: Session, email: str) -> Optional[Aluno]:
        """
        Obter aluno por email (útil para validações).
        
        Args:
            db: Sessão do banco de dados
            email: Email do aluno
        
        Returns:
            Optional[Aluno]: Aluno encontrado ou None
        """
        return db.query(Aluno).filter(Aluno.email == email).first()

    @staticmethod
    def obter_aluno_por_matricula(db: Session, matricula: str) -> Aluno:
        """
        Obter aluno por número de matrícula.
        
        Args:
            db: Sessão do banco de dados
            matricula: Número de matrícula
        
        Returns:
            Aluno: Objeto aluno encontrado
        
        Raises:
            HTTPException: Se aluno não encontrado (404)
        """
        aluno = db.query(Aluno).filter(Aluno.matricula == matricula).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        return aluno

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, aluno_update: AlunoUpdate) -> Aluno:
        """
        Atualizar dados de um aluno existente.
        
        Atualiza apenas os campos fornecidos (exclude_unset=True).
        Valida unicidade de email e matrícula.
        
        Args:
            db: Sessão do banco de dados
            aluno_id: ID do aluno a atualizar
            aluno_update: Dados atualizados (AlunoUpdate)
        
        Returns:
            Aluno: Objeto aluno atualizado
        
        Raises:
            HTTPException: Se aluno não encontrado (404) ou email duplicado (400)
        
        Example:
            >>> update_data = AlunoUpdate(periodo=2)
            >>> aluno_atualizado = AlunoService.atualizar_aluno(db, 1, update_data)
        """
        db_aluno = AlunoService.obter_aluno_por_id(db, aluno_id)
        
        dados_atualizacao = aluno_update.dict(exclude_unset=True)
        for campo, valor in dados_atualizacao.items():
            setattr(db_aluno, campo, valor)
        
        try:
            db.commit()
            db.refresh(db_aluno)
            logger.info(f"✓ Aluno {aluno_id} atualizado")
            return db_aluno
        except IntegrityError:
            db.rollback()
            logger.error(f"✗ Erro ao atualizar aluno {aluno_id}: Email duplicado")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )

    @staticmethod
    def deletar_aluno(db: Session, aluno_id: int) -> None:
        """
        Remover um aluno do banco de dados.
        
        Cascata remove matrículas relacionadas automaticamente.
        
        Args:
            db: Sessão do banco de dados
            aluno_id: ID do aluno a deletar
        
        Raises:
            HTTPException: Se aluno não encontrado (404)
        
        Example:
            >>> AlunoService.deletar_aluno(db, aluno_id=1)
        """
        db_aluno = AlunoService.obter_aluno_por_id(db, aluno_id)
        db.delete(db_aluno)
        db.commit()
        logger.info(f"✓ Aluno {aluno_id} deletado")
