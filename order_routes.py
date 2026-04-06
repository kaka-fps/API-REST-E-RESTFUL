from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import SolicitSchema
from models import Solicit, User

order_router = APIRouter(prefix="/requests", tags=["requests"], dependencies=[Depends(verify_token)])

@order_router.get("/")
async  def solicits():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """ 
    return {"mensage": "Você acessou a rota de pedidos"}

@order_router.post("/order")
async def create_Solicit(Solicit_schema: SolicitSchema, session: Session = Depends(get_session)):
    new_solicit = Solicit(user_id=Solicit_schema.user)
    session.add(new_solicit)
    session.commit()
    return {"mensagem": f"pedido criado com sucesso. ID do pedido: {new_solicit.id} "}


@order_router.post("/Solicit/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
# usuario.adim = True
# usuario.id = pedido.usuario 
    order = session.query(Solicit).filter(Solicit.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="pedido não encontrado")
    if not user.admin or user.id != order.user_id:
        raise HTTPException(status_code=401, detail="você não tem autorização para fazer essa modificação")
    order.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero: {order.id} cancelado cancelado com sucesso",
        "pedido": order
    }
