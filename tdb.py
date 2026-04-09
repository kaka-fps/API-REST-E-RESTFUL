
from models import Solicit, ItemOrder
from models import db
from sqlalchemy.orm import sessionmaker, Session

SessionLocal = sessionmaker(bind=db)
session = SessionLocal()

session.query(ItemOrder).filter(ItemOrder.id == 1).delete()
session.commit()



# feito por pura preguiça de mecher com banco de dados de outras maneiras o famoso (quem não tem cão caça com gato)