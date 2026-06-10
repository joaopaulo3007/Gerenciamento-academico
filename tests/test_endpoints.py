"""
Testes Unitários - Endpoints da API

Testes para validar funcionalidade dos principais endpoints.

Executar com:
    pytest tests/test_endpoints.py -v

Author: Sistema Acadêmico
Version: 1.0.0
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db
from app.domain.models import Base


# Configurar banco de testes em memória
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override do get_db para usar banco de testes."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


class TestHealth:
    """Testes para endpoint de health check."""
    
    def test_health_check(self):
        """Testar se health check retorna status online."""
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["database"] == "connected"
        assert data["version"] == "1.0.0"


class TestAlunos:
    """Testes para endpoints de alunos."""
    
    def test_criar_aluno(self):
        """Testar criação de um novo aluno."""
        aluno_data = {
            "nome": "João Silva",
            "email": "joao@test.com",
            "matricula": "2024001",
            "periodo": 1
        }
        response = client.post("/v1/alunos", json=aluno_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "João Silva"
        assert data["email"] == "joao@test.com"
        assert data["id"] == 1
    
    def test_criar_aluno_email_duplicado(self):
        """Testar se não permite email duplicado."""
        aluno_data = {
            "nome": "Maria Santos",
            "email": "maria@test.com",
            "matricula": "2024002",
            "periodo": 2
        }
        # Primeiro
        client.post("/v1/alunos", json=aluno_data)
        # Segundo (duplicado)
        response = client.post("/v1/alunos", json={
            **aluno_data,
            "matricula": "2024003"
        })
        assert response.status_code == 400
        assert "já cadastrados" in response.json()["detail"]
    
    def test_listar_alunos(self):
        """Testar listagem de alunos."""
        response = client.get("/v1/alunos")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_obter_aluno_por_id(self):
        """Testar obtenção de aluno por ID."""
        aluno_data = {
            "nome": "Pedro Costa",
            "email": "pedro@test.com",
            "matricula": "2024004",
            "periodo": 1
        }
        # Criar aluno
        response_create = client.post("/v1/alunos", json=aluno_data)
        aluno_id = response_create.json()["id"]
        
        # Obter aluno
        response = client.get(f"/v1/alunos/{aluno_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "Pedro Costa"
        assert data["id"] == aluno_id
    
    def test_obter_aluno_inexistente(self):
        """Testar erro ao obter aluno inexistente."""
        response = client.get("/v1/alunos/9999")
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"]
    
    def test_atualizar_aluno(self):
        """Testar atualização de aluno."""
        # Criar aluno
        aluno_data = {
            "nome": "Ana Silva",
            "email": "ana@test.com",
            "matricula": "2024005",
            "periodo": 1
        }
        response_create = client.post("/v1/alunos", json=aluno_data)
        aluno_id = response_create.json()["id"]
        
        # Atualizar
        update_data = {"periodo": 3}
        response = client.put(f"/v1/alunos/{aluno_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["periodo"] == 3
    
    def test_deletar_aluno(self):
        """Testar deleção de aluno."""
        # Criar aluno
        aluno_data = {
            "nome": "Carlos Santos",
            "email": "carlos@test.com",
            "matricula": "2024006",
            "periodo": 2
        }
        response_create = client.post("/v1/alunos", json=aluno_data)
        aluno_id = response_create.json()["id"]
        
        # Deletar
        response = client.delete(f"/v1/alunos/{aluno_id}")
        assert response.status_code == 204
        
        # Verificar se foi deletado
        response_get = client.get(f"/v1/alunos/{aluno_id}")
        assert response_get.status_code == 404


class TestProfessores:
    """Testes para endpoints de professores."""
    
    def test_criar_professor(self):
        """Testar criação de professor."""
        professor_data = {
            "nome": "Dra. Maria Santos",
            "email": "maria@professor.com",
            "especialidade": "Engenharia de Software"
        }
        response = client.post("/v1/professores", json=professor_data)
        assert response.status_code == 201
        data = response.json()
        assert data["nome"] == "Dra. Maria Santos"
        assert data["email"] == "maria@professor.com"
    
    def test_listar_professores(self):
        """Testar listagem de professores."""
        response = client.get("/v1/professores")
        assert response.status_code == 200
        assert isinstance(response.json(), list)


class TestRoot:
    """Testes para endpoint raiz."""
    
    def test_root_endpoint(self):
        """Testar endpoint raiz."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "docs" in data


# Executar testes
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
