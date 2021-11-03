from app.models.base import Base
from sqlalchemy import Column, Integer, String


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='无名')
    isbn = Column(String(15), nullable=False, unique=True)
    price = Column(String(20))
    binding = Column(String(20))
    publisher = Column(String(50))
    pubdate = Column(String(20))
    summary = Column(String(1000))
    image = Column(String(50))

    def sample(self):
        pass

