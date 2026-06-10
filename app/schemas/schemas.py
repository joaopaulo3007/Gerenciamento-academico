from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum as PyEnum


class StatusMatriculaEnum(str, PyEnum):
    ATIVA = "ativa"
    CANCELADA = "cancelada"
    CONCLUIDA = "concluída"


class TipoNotaEnum(str, PyEnum):
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"
    FINAL = "Final"


# ===== ALUNO =====
class AlunoCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    matricula: str = Field(..., min_length=5, max_length=20)
    periodo: int = Field(..., ge=1, le=8)

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "João Paulo Felisardo",
                "email": "joaopaulodemoraesfelisardo@gmail.com",
                "matricula": "2301045",
                "periodo": 1,
            }
        }


class AlunoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    periodo: Optional[int] = Field(None, ge=1, le=8)


class AlunoResponse(AlunoCreate):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== PROFESSOR =====
class ProfessorCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    email: EmailStr
    especialidade: str = Field(..., min_length=3, max_length=100)

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Roger",
                "email": "roger@anchieta.com",
                "especialidade": "Arquitetura de Software",
            }
        }


class ProfessorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    email: Optional[EmailStr] = None
    especialidade: Optional[str] = Field(None, min_length=3, max_length=100)


class ProfessorResponse(ProfessorCreate):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== DISCIPLINA =====
class DisciplinaCreate(BaseModel):
    nome: str = Field(..., min_length=3, max_length=150)
    codigo: str = Field(..., min_length=3, max_length=20)
    carga_horaria: int = Field(..., ge=10, le=200)
    professor_id: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "Arquitetura de Software",
                "codigo": "ASW001",
                "carga_horaria": 60,
                "professor_id": 1,
            }
        }


class DisciplinaUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=150)
    carga_horaria: Optional[int] = Field(None, ge=10, le=200)
    professor_id: Optional[int] = Field(None, gt=0)


class DisciplinaResponse(DisciplinaCreate):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== TURMA =====
class TurmaCreate(BaseModel):
    disciplina_id: int = Field(..., gt=0)
    semestre: int = Field(..., ge=1, le=2)
    ano: int = Field(..., ge=2020, le=2100)
    vagas: int = Field(..., ge=1, le=100)

    class Config:
        json_schema_extra = {
            "example": {
                "disciplina_id": 1,
                "semestre": 1,
                "ano": 2024,
                "vagas": 30,
            }
        }


class TurmaUpdate(BaseModel):
    vagas: Optional[int] = Field(None, ge=1, le=100)


class TurmaResponse(TurmaCreate):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== MATRÍCULA =====
class MatriculaCreate(BaseModel):
    aluno_id: int = Field(..., gt=0)
    turma_id: int = Field(..., gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "aluno_id": 1,
                "turma_id": 1,
            }
        }


class MatriculaUpdate(BaseModel):
    status: Optional[StatusMatriculaEnum] = None


class MatriculaResponse(BaseModel):
    id: int
    aluno_id: int
    turma_id: int
    data_matricula: datetime
    status: StatusMatriculaEnum
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== NOTA =====
class NotaCreate(BaseModel):
    matricula_id: int = Field(..., gt=0)
    tipo: TipoNotaEnum
    valor: float = Field(..., ge=0, le=10)

    class Config:
        json_schema_extra = {
            "example": {
                "matricula_id": 1,
                "tipo": "N1",
                "valor": 8.5,
            }
        }


class NotaUpdate(BaseModel):
    valor: float = Field(..., ge=0, le=10)


class NotaResponse(NotaCreate):
    id: int
    data_lancamento: datetime
    data_criacao: datetime

    class Config:
        from_attributes = True


# ===== BOLETIM (Relatório) =====
class BoletimDisciplinaResponse(BaseModel):
    disciplina_nome: str
    disciplina_codigo: str
    professor_nome: str
    notas: List[NotaResponse]
    media: float

    class Config:
        json_schema_extra = {
            "example": {
                "disciplina_nome": "Arquitetura de Software",
                "disciplina_codigo": "ASW001",
                "professor_nome": "Roger",
                "notas": [
                    {"id": 1, "matricula_id": 1, "tipo": "N1", "valor": 8.5, "data_lancamento": "2024-06-10T10:30:00", "data_criacao": "2024-06-10T10:30:00"},
                ],
                "media": 8.5,
            }
        }


class BoletimResponse(BaseModel):
    aluno_id: int
    aluno_nome: str
    aluno_matricula: str
    disciplinas: List[BoletimDisciplinaResponse]
    media_geral: float

    class Config:
        json_schema_extra = {
            "example": {
                "aluno_id": 1,
                "aluno_nome": "João Paulo Felisardo",
                "aluno_matricula": "2301045",
                "disciplinas": [],
                "media_geral": 0.0,
            }
        }


# ===== HEALTH =====
class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "online",
                "database": "connected",
                "version": "1.0.0",
                "timestamp": "2024-06-10T10:30:00",
            }
        }
