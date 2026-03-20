from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_session
from schemas import RequestSchema
from models import request

order_router = APIRouter(prefix="/requests", tags=["requests"])

@order_router.get("/")
async  def requests():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """ 
    return {"mensage": "Você acessou a rota de pedidos"}

@order_router.post("/request")
async def create_request(request_schema: RequestSchema, session: Session = Depends(get_session)):
    new_request = request(user=RequestSchema.id_user)
    session.add(new_request)
    session.commit()
    return {"mensagem": f"pedido criado com sucesso. ID do pedido: {new_request.id} "}

