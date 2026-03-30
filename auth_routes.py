from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINITES, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def create_token(id_user, duration_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINITES)):
    expiration_date = datetime.now(timezone.utc) + duration_token
    dic_info = {"sub": id_user, "exp": expiration_date}
    jwt_encoded = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_encoded

def verify_token(token, session: Session = Depends(get_session)):
    # verificar se o token é valido
    # extrair o ID do usuario do token
    user = session.query(User).filter(User.id==1).first()
    return user

def autenty_user(email, password, session):
    user = session.query(User).filter(User.email==email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    
    return user


@auth_router.get("/")
async  def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensage": "Você acessou a rota de padrão de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")
async  def criar_conta(user_schema: UserSchema, session: Session = Depends(get_session)):
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
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = autenty_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais invalidas")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, duration_token=timedelta(days=7))
        return {"access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
                }
#JWT Bearer 
# headers = {"Access-Token": "dearer token"}

@auth_router.get("/refresh")
async def user_refresh_token(token):
    #verificar o token
    user = verify_token(token)
    access_token = create_token(user.id)