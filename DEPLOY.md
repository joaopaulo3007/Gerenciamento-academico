# 🚀 Guia de Deploy no GitHub

## Pré-requisitos
- Conta GitHub
- Git instalado localmente
- Acesso ao terminal

## Passo 1: Criar Repositório no GitHub

1. Acesse [github.com/new](https://github.com/new)
2. Nome: `academico-api`
3. Descrição: `API REST de gerenciamento acadêmico com FastAPI`
4. Escolha: Public (para avaliação)
5. **Não** inicie com README, .gitignore ou license
6. Clique "Create repository"

## Passo 2: Conectar Repositório Local ao GitHub

```bash
cd c:\Users\JoãoPaulodeMoraesFel\Desktop\academico-api

# Adicionar remote (substitua YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/academico-api.git

# Renomear branch para main (se necessário)
git branch -M main

# Push do código
git push -u origin main
```

## Passo 3: Verificar Push

Acesse `https://github.com/YOUR_USERNAME/academico-api` e verifique se todos os arquivos estão lá.

## Estrutura de Arquivos no Repositório

```
academico-api/
├── README.md ✓
├── FLUXOGRAMA.md ✓
├── Dockerfile ✓
├── docker-compose.yml ✓
├── requirements.txt ✓
├── pyproject.toml ✓
├── .gitignore ✓
├── .env.example ✓
└── app/ ✓
    ├── main.py
    ├── domain/ (models.py)
    ├── schemas/ (schemas.py)
    ├── services/ (6 services)
    ├── router/ (6 routers)
    └── database/ (connection.py, seed.py)
```

## Testando o Projeto

Após clonar do GitHub em qualquer máquina:

```bash
git clone https://github.com/YOUR_USERNAME/academico-api.git
cd academico-api

# Subir com Docker
docker-compose up --build

# Acessar
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
```

## ✅ Checklist Final

- [x] Código implementado
- [x] Git inicializado
- [x] README completo
- [x] Fluxograma criado
- [x] Docker configurado
- [x] Seed com dados
- [x] Repositório criado no GitHub
- [x] Push realizado
- [x] Link do repositório enviado pelo portal

## 📝 Informações para Entregar

**Link do Repositório**: `https://github.com/YOUR_USERNAME/academico-api`

**Comandos para Executar**:
```bash
git clone https://github.com/YOUR_USERNAME/academico-api.git
cd academico-api
docker-compose up --build
```

**URLs após iniciar**:
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health: http://localhost:8000/v1/health

---

**Data de Entrega**: 19/06/2026

Bom sorte! 🎓
