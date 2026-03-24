from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async  def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensage": "Você acessou a rota de padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async  def criar_conta(user_schema: UserSchema, session = Depends(get_session)):
    user = session.query(User).filter(User.email==user_schema.email).first()
    if user:
        raise HTTPException(status_code=400, detail="E-mail do usuario já cadastrado")
    else:
        password_criptograpy = bcrypt_context.hash(user_schema.password)
        new_user = User(user_schema.name, user_schema.email, password_criptograpy, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"mensagem": f"usuario cadastrado com sucesso {user_schema.email} "}

# login -> email e senha -> token JWT (Json Web Token) dchfiodbhcvucpnc034m2mmic0cv