from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy import Enum

# criar a conexão do seu banco
db = create_engine("sqlite:///banco.db")

# criar a base do banco de de dados
Base = declarative_base()

#criar as classes/tabelas do banco

class User(Base):
    __tablename__="user"

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

class Solicit(Base):
    __tablename__="solicit"

#    STATUS_PEDIDOS = [
#    ("PENDENTE", "Pendente"),
#    ("CANCELADO", "Cancelado"),
#    ("FINALIZADO", "Finalizado")
#]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #pendente, cancelado, finalizado
    user_id  = Column("user", ForeignKey("user.id"))
    price = Column("price", Float,)
    itens = relationship("ItemOrder", back_populates="solicit", cascade="all, delete")

    def __init__(self, user_id, status="PENDENTE", price=0):
        self.user_id = user_id
        self.price = price
        self.status = status

    def calculate_price(self):
        # percorrer todos os itens do pedido
        # somar todos os precos de todos os itens do pedido
        # editar no campo "preço" o valor final do pedido


        price_order = 0
        for item in self.itens:
            price_item = item.price_unit * item.amount 
            price_order += price_item


        # self.price = sum(item.price_unit * item.amount for item in self.itens)

#itenspedido

class ItemOrder(Base):
    __tablename__="itens_order"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String) 
    price_unit = Column("price_unit", Float)
    solicit_id = Column("solicit", ForeignKey("solicit.id"))

    solicit = relationship("Solicit", back_populates="itens")

    def __init__(self, amount, flavor, size, price_unit, solicit):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.price_unit = price_unit
        self.solicit = solicit

# executa a criação dos metadados do seu banco (criar efetivamente o banco de dados)

# migrar o banco de dados 

# criar a migração: alembic revision --autogenerate -m "mensagem"
#executar a migração: alembic upgrade head
