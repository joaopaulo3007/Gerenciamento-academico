from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    matricula = Column(String(20), unique=True, nullable=False, index=True)
    periodo = Column(Integer, nullable=False)  # 1º, 2º, 3º... período
    data_criacao = Column(DateTime, default=datetime.utcnow)

    matriculas = relationship("Matricula", back_populates="aluno", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Aluno(id={self.id}, nome={self.nome}, matricula={self.matricula})>"


class Professor(Base):
    __tablename__ = "professores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    especialidade = Column(String(100), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    disciplinas = relationship("Disciplina", back_populates="professor")

    def __repr__(self):
        return f"<Professor(id={self.id}, nome={self.nome}, especialidade={self.especialidade})>"


class Disciplina(Base):
    __tablename__ = "disciplinas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    carga_horaria = Column(Integer, nullable=False)  # em horas
    professor_id = Column(Integer, ForeignKey("professores.id"), nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    professor = relationship("Professor", back_populates="disciplinas")
    turmas = relationship("Turma", back_populates="disciplina", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Disciplina(id={self.id}, nome={self.nome}, codigo={self.codigo})>"


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    semestre = Column(Integer, nullable=False)  # 1º, 2º semestre
    ano = Column(Integer, nullable=False)
    vagas = Column(Integer, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    disciplina = relationship("Disciplina", back_populates="turmas")
    matriculas = relationship("Matricula", back_populates="turma", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Turma(id={self.id}, disciplina_id={self.disciplina_id}, ano={self.ano})>"


class StatusMatricula(str, enum.Enum):
    ATIVA = "ativa"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluída"


class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    turma_id = Column(Integer, ForeignKey("turmas.id"), nullable=False)
    data_matricula = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(StatusMatricula), default=StatusMatricula.ATIVA, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    aluno = relationship("Aluno", back_populates="matriculas")
    turma = relationship("Turma", back_populates="matriculas")
    notas = relationship("Nota", back_populates="matricula", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Matricula(id={self.id}, aluno_id={self.aluno_id}, turma_id={self.turma_id})>"


class TipoNota(str, enum.Enum):
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"
    FINAL = "Final"


class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    matricula_id = Column(Integer, ForeignKey("matriculas.id"), nullable=False)
    tipo = Column(Enum(TipoNota), nullable=False)
    valor = Column(Float, nullable=False)  # 0 a 10
    data_lancamento = Column(DateTime, default=datetime.utcnow)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    matricula = relationship("Matricula", back_populates="notas")

    def __repr__(self):
        return f"<Nota(id={self.id}, matricula_id={self.matricula_id}, tipo={self.tipo}, valor={self.valor})>"
