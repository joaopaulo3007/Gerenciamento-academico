from sqlalchemy.orm import Session
from app.domain.models import Aluno, Matricula, Nota, Turma, Disciplina, Professor
from app.schemas import BoletimResponse, BoletimDisciplinaResponse, NotaResponse
from typing import Optional
from fastapi import HTTPException, status


class RelatorioService:
    @staticmethod
    def gerar_boletim(db: Session, aluno_id: int) -> BoletimResponse:
        """Gerar boletim do aluno com notas e média"""
        # Verificar se aluno existe
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aluno não encontrado"
            )
        
        # Obter todas as matrículas ativas do aluno
        matriculas = db.query(Matricula).filter(
            Matricula.aluno_id == aluno_id,
            Matricula.status == "ativa"
        ).all()
        
        disciplinas_info = []
        todas_as_notas = []
        
        for matricula in matriculas:
            turma = db.query(Turma).filter(Turma.id == matricula.turma_id).first()
            disciplina = db.query(Disciplina).filter(Disciplina.id == turma.disciplina_id).first()
            professor = db.query(Professor).filter(Professor.id == disciplina.professor_id).first()
            
            # Obter notas da matrícula
            notas = db.query(Nota).filter(Nota.matricula_id == matricula.id).all()
            todas_as_notas.extend(notas)
            
            # Calcular média da disciplina
            if notas:
                media_disciplina = sum(n.valor for n in notas) / len(notas)
            else:
                media_disciplina = 0.0
            
            notas_response = [
                NotaResponse.from_orm(n) for n in notas
            ]
            
            disciplina_info = BoletimDisciplinaResponse(
                disciplina_nome=disciplina.nome,
                disciplina_codigo=disciplina.codigo,
                professor_nome=professor.nome,
                notas=notas_response,
                media=media_disciplina
            )
            
            disciplinas_info.append(disciplina_info)
        
        # Calcular média geral
        if todas_as_notas:
            media_geral = sum(n.valor for n in todas_as_notas) / len(todas_as_notas)
        else:
            media_geral = 0.0
        
        return BoletimResponse(
            aluno_id=aluno.id,
            aluno_nome=aluno.nome,
            aluno_matricula=aluno.matricula,
            disciplinas=disciplinas_info,
            media_geral=media_geral
        )
