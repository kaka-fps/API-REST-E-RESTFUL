from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import SolicitSchema
from models import Solicit

order_router = APIRouter(prefix="/requests", tags=["requests"])

@order_router.get("/")
async  def solicits():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """ 
    return {"mensage": "Você acessou a rota de pedidos"}

@order_router.post("/solicit")
async def create_Solicit(Solicit_schema: SolicitSchema, session: Session = Depends(get_session)):
    new_solicit = Solicit(user=Solicit_schema.user)
    session.add(new_solicit)
    session.commit()
    return {"mensagem": f"pedido criado com sucesso. ID do pedido: {new_solicit.id} "}

