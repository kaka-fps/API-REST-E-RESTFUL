from fastapi import APIRouter
from models import User, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async  def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensage": "Você acessou a rota de padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async  def criar_conta(email: str, senha: str, name: str):
    Session = sessionmaker(bind = db)
    Session = Session()
    user = Session.query(User).filter(User.email==email).first()
    if user:
        return {"mensagem": "usuario je existe com esse email"}
    else:
        new_user = User(name, email, senha)
        Session.add(new_user)
        Session.commit()
        return {"mensagem": "usuario cadastrado com sucesso"}