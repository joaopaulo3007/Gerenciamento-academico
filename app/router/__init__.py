from .aluno_router import router as aluno_router
from .professor_router import router as professor_router
from .disciplina_router import router as disciplina_router
from .matricula_router import router as matricula_router
from .nota_router import router as nota_router
from .relatorio_router import router as relatorio_router

__all__ = [
    "aluno_router",
    "professor_router",
    "disciplina_router",
    "matricula_router",
    "nota_router",
    "relatorio_router",
]
