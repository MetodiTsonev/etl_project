from fastapi import FastAPI, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import date as date_type, datetime
from utils.database import SessionLocal, engine
from utils.models import Base, Article
from utils import schemas
import json
import logging

logging.basicConfig(level=logging.INFO)


app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/articles/", response_model=List[schemas.ArticleInDB])
def get_articles(page: int = 1, db: Session = Depends(get_db)):
    articles_per_page = 5
    offset = (page - 1) * articles_per_page
    articles = db.query(Article).offset(offset).limit(articles_per_page).all()

    if not articles:
        raise HTTPException(status_code=404, detail="No articles found")

    for article in articles:
        article.images = json.loads(article.images)
        article.body = json.loads(article.body)

    return articles

@app.get("/articles/by_date/", response_model=List[schemas.ArticleInDB])
def get_articles_by_date(date: date_type, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.publication_date == date).all()

    if not articles:
        raise HTTPException(status_code=404, detail=f"No articles found for date {date}")

    for article in articles:
        article.images = json.loads(article.images)
        article.body = json.loads(article.body)

    return articles

@app.get("/articles/by_author/", response_model=List[schemas.ArticleInDB])
def get_articles_by_author(author: str, db: Session = Depends(get_db)):
    articles = db.query(Article).filter(Article.author == author).all()

    if not articles:
        raise HTTPException(status_code=404, detail=f"No articles found for author {author}")

    for article in articles:
        article.images = json.loads(article.images)
        article.body = json.loads(article.body)

    return articles


@app.get("/article/{article_UID}", response_model=schemas.ArticleInDB)
def get_article(article_UID: int = Path(..., title="The ID of the article to retrieve"), db: Session = Depends(get_db)):
    logging.info(f"Fetching article with ID: {article_UID}")

    article = db.query(Article).filter(Article.id == article_UID).first()

    if article is None:
        logging.error(f"Article with ID {article_UID} not found")
        raise HTTPException(status_code=404, detail=f"Article with ID {article_UID} not found")

    logging.info(f"Article found: {article}")

    article.images = json.loads(article.images)
    article.body = json.loads(article.body)

    return article

@app.post("/article/{article_UID}", response_model=schemas.ArticleInDB)
def create_article(article_UID: int, article: schemas.ArticleBase, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == article_UID).first()
    if db_article:
        raise HTTPException(status_code=400, detail="Article with this ID already exists")

    new_article = Article(
        id=article_UID,
        author=article.author,
        title=article.title,
        publication_date=article.publication_date,
        url=article.url,
        images=json.dumps(article.images),
        body=json.dumps(article.body)
    )

    try:
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to create the article")

    new_article.images = json.loads(new_article.images)
    new_article.body = json.loads(new_article.body)

    return new_article

@app.delete("/article/{article_id}", response_model=dict)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully", "article_id": article_id}

@app.put("/article/{article_id}", response_model=dict)
def update_article(article_id: int, article_update: schemas.ArticleInDB, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")

    try:
        publication_date = datetime.strptime(article_update.publication_date, '%Y-%m-%d').date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")

    article.author = article_update.author
    article.title = article_update.title
    article.publication_date = publication_date
    article.url = article_update.url
    article.images = json.dumps(article_update.images)
    article.body = json.dumps(article_update.body)

    try:
        db.commit()
        db.refresh(article)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update article: {e}")

    return {"message": "Article updated successfully", "article": article_update.dict()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)