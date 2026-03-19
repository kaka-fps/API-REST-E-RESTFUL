from fastapi import APIRouter, Depends
from models import User
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async  def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensage": "Você acessou a rota de padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async  def criar_conta(email: str, password: str, name: str, session = Depends(get_session)):
    user = session.query(User).filter(User.email==email).first()
    if user:
        return {"mensagem": "usuario je existe com esse email"}
    else:
        password_criptograpy = bcrypt_context.hash(password)
        new_user = User(name, email, password_criptograpy)
        session.add(new_user)
        session.commit()
        return {"mensagem": "usuario cadastrado com sucesso"}