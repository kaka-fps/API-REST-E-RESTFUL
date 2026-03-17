from fastapi import APIRouter

order_router = APIRouter(prefix="/request", tags=["request"])

@order_router.get("/")
async  def request():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """ 
    return {"mensage": "Você acessou a rota de pedidos"}