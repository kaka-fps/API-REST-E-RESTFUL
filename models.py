from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import Enum

# criar a conexão do seu banco
db = create_engine("sqlite:///banco.db")

# criar a base do banco de de dados
Base = declarative_base()

#criar as classes/tabelas do banco

class User(Base):
    __tablename__="usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password",Integer)
    active = Column("active",Boolean)
    admin = Column("admin",Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin

# padidos

class request(Base):
    __tablename__="pedidos"

#    STATUS_PEDIDOS = [
#    ("PENDENTE", "Pendente"),
#    ("CANCELADO", "Cancelado"),
#    ("FINALIZADO", "Finalizado")
#]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    user = Column("user", ForeignKey("usuarios.id"))
    price = Column("price", Float,)
    # itens = Column("itens",)

    def __init__(self, user, status="PENDENTE", price=0):
        self.user = user
        self.price = price
        self.status = status

#itenspedido

class ItemRequest(Base):
    __tablename__="itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    price_unit = Column("price_unit", Float)
    request = Column("request", ForeignKey("requests.id"))

    def __init__(self, amount, flavor, size, price_unit, request):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.price_unit = price_unit
        self.request = request

# executa a criação dos metadados do seu banco (criar efetivamente o banco de dados)
