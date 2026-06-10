from sqlalchemy.orm import Session
from app.domain.models import Aluno, Professor, Disciplina, Turma, Matricula, Nota, StatusMatricula, TipoNota
from datetime import datetime, timedelta
import random


def seed_database(db: Session):
    """Popula o banco de dados com dados de exemplo"""
    
    # Verificar se dados já existem
    if db.query(Professor).count() > 0:
        return

    # ===== CRIAR PROFESSORES =====
    professor1 = Professor(
        nome="Roger",
        email="roger@anchieta.com",
        especialidade="Arquitetura de Software"
    )
    professor2 = Professor(
        nome="Prof. Carlos Oliveira",
        email="carlos.oliveira@academico.com",
        especialidade="Banco de Dados"
    )
    professor3 = Professor(
        nome="Profa. Ana Costa",
        email="ana.costa@academico.com",
        especialidade="Algoritmos e Estruturas de Dados"
    )

    db.add_all([professor1, professor2, professor3])
    db.flush()  # Para obter os IDs gerados

    # ===== CRIAR ALUNOS =====
    alunos_data = [
        {"nome": "João Paulo Felisardo", "email": "joaopaulodemoraesfelisardo@gmail.com", "matricula": "2301045", "periodo": 3},
        {"nome": "Maria Oliveira", "email": "maria.oliveira@aluno.com", "matricula": "2024002", "periodo": 2},
        {"nome": "Pedro Santos", "email": "pedro.santos@aluno.com", "matricula": "2024003", "periodo": 1},
        {"nome": "Lucas Ferreira", "email": "lucas.ferreira@aluno.com", "matricula": "2024004", "periodo": 4},
        {"nome": "Ana Carolina", "email": "ana.carolina@aluno.com", "matricula": "2024005", "periodo": 2},
    ]
    
    alunos = [Aluno(**data) for data in alunos_data]
    db.add_all(alunos)
    db.flush()

    # ===== CRIAR DISCIPLINAS =====
    disciplinas_data = [
        {
            "nome": "Arquitetura de Software",
            "codigo": "ASW001",
            "carga_horaria": 60,
            "professor_id": professor1.id,
        },
        {
            "nome": "Banco de Dados Relacional",
            "codigo": "BD001",
            "carga_horaria": 45,
            "professor_id": professor2.id,
        },
        {
            "nome": "Algoritmos e Estruturas de Dados",
            "codigo": "AED001",
            "carga_horaria": 75,
            "professor_id": professor3.id,
        },
        {
            "nome": "Engenharia de Software Avançada",
            "codigo": "ES002",
            "carga_horaria": 90,
            "professor_id": professor2.id,
        },
    ]
    
    disciplinas = [Disciplina(**data) for data in disciplinas_data]
    db.add_all(disciplinas)
    db.flush()

    # ===== CRIAR TURMAS =====
    turmas_data = [
        {"disciplina_id": disciplinas[0].id, "semestre": 1, "ano": 2024, "vagas": 30},
        {"disciplina_id": disciplinas[1].id, "semestre": 1, "ano": 2024, "vagas": 25},
        {"disciplina_id": disciplinas[2].id, "semestre": 2, "ano": 2024, "vagas": 35},
        {"disciplina_id": disciplinas[3].id, "semestre": 2, "ano": 2024, "vagas": 20},
    ]
    
    turmas = [Turma(**data) for data in turmas_data]
    db.add_all(turmas)
    db.flush()

    # ===== CRIAR MATRÍCULAS =====
    matricula_configs = [
        (alunos[0], turmas[0]),  # João em Python
        (alunos[0], turmas[1]),  # João em BD
        (alunos[0], turmas[2]),  # João em AED
        (alunos[1], turmas[0]),  # Maria em Python
        (alunos[1], turmas[1]),  # Maria em BD
        (alunos[2], turmas[0]),  # Pedro em Python
        (alunos[2], turmas[2]),  # Pedro em AED
        (alunos[3], turmas[1]),  # Lucas em BD
        (alunos[3], turmas[3]),  # Lucas em ES2
        (alunos[4], turmas[0]),  # Ana em Python
        (alunos[4], turmas[2]),  # Ana em AED
    ]
    
    matriculas = []
    for aluno, turma in matricula_configs:
        matricula = Matricula(
            aluno_id=aluno.id,
            turma_id=turma.id,
            status=StatusMatricula.ATIVA,
            data_matricula=datetime.utcnow() - timedelta(days=random.randint(10, 60)),
        )
        matriculas.append(matricula)
    
    db.add_all(matriculas)
    db.flush()

    # ===== CRIAR NOTAS =====
    notas = []
    for matricula in matriculas:
        # N1
        notas.append(Nota(
            matricula_id=matricula.id,
            tipo=TipoNota.N1,
            valor=round(random.uniform(6.0, 10.0), 1),
            data_lancamento=datetime.utcnow() - timedelta(days=random.randint(5, 30)),
        ))
        # N2
        notas.append(Nota(
            matricula_id=matricula.id,
            tipo=TipoNota.N2,
            valor=round(random.uniform(6.0, 10.0), 1),
            data_lancamento=datetime.utcnow() - timedelta(days=random.randint(1, 20)),
        ))
        # N3 (opcional - nem todos têm)
        if random.choice([True, False]):
            notas.append(Nota(
                matricula_id=matricula.id,
                tipo=TipoNota.N3,
                valor=round(random.uniform(5.0, 10.0), 1),
                data_lancamento=datetime.utcnow() - timedelta(days=random.randint(1, 10)),
            ))
    
    db.add_all(notas)
    db.commit()
