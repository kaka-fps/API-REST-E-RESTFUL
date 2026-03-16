from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async  def auth():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensage": "Você acessou a rota de padrão de autenticação", "autenticado": False}