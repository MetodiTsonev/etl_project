from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ArticleBase(BaseModel):
    author: Optional[str] = None
    title: str
    publication_date: date
    url: str
    images: List[str]
    body: List[str]

class ArticleInDB(ArticleBase):
    id: int

    class Config:
        orm_mode = True