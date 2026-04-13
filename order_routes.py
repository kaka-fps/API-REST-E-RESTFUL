from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from schemas import SolicitSchema, ItemorderSchema
from models import Solicit, User, ItemOrder

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

@order_router.get("/list")
async def list_order(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if not user.admin:
        raise  HTTPException(status_code=401, detail="você não tem autorização para fazer essa operação")
    else:
        solicits = session.query(Solicit).all()
        return {
            "pedidos" : solicits
        }

@order_router.post("/order/add-item/{id_order}")
async def add_item_order(id_order: int,
                        item_order_schema: ItemorderSchema,
                        session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    solicit = session.query(Solicit).filter(Solicit.id==id_order).first()
    if not solicit:
        raise  HTTPException(status_code=400, detail="pedido não existe")
    if not user.admin and user.id != solicit.user_id:
        raise  HTTPException(status_code=401, detail="você não tem autorização para fazer essa operação")
    item_order = ItemOrder(
        item_order_schema.amount,
        item_order_schema.flavor,
        item_order_schema.size,
        item_order_schema.price_unit,
        solicit)
    session.add(item_order)
    session.flush()
    
    solicit.calculate_price()
    
    session.commit()
    return {
        "mensagem": "item criado com sucesso",
        "item_id": item_order,
        "preço_pedido": solicit.price
    }

@order_router.post("/order/remove-item/{id_item_order}")
async def remove_item_order(id_item_order: int,
                        session: Session = Depends(get_session),
                        user: User = Depends(verify_token)):
    item_order = session.query(ItemOrder).filter(ItemOrder.id==id_item_order).first()
    if not item_order:
        raise  HTTPException(status_code=400, detail="item no pedido não existe")
    if not user.admin and user.id != item_order.user_id:
        raise  HTTPException(status_code=401, detail="você não tem autorização para fazer essa operação")
    session.delete(item_order)
    session.flush()
    
    item_order.solicit.calculate_price()
    
    session.commit()
    return {
        "mensagem": "item removido com sucesso",
        "pedido": item_order.solicit
    }
