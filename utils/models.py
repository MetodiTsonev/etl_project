from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.types import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True, index=True)
    author = Column(String, index=True)
    title = Column(String, index=True)
    publication_date = Column(Date)
    url = Column(String, unique=True, index=True)
    images = Column(JSON)
    body = Column(JSON)