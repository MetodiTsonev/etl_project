import json
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from utils.database import engine, SessionLocal
from utils.models import Article

class ScrapyProjectPipeline:
    def __init__(self):
        self.Session = SessionLocal

    def process_item(self, item, spider):
        session = self.Session()
        publication_date = item.get('publication_date')
        if publication_date:
            try:
                date_part = publication_date.split('T')[0]
                publication_date = datetime.strptime(date_part, '%Y-%m-%d').date()
            except (ValueError, TypeError) as e:
                spider.logger.error(f"Failed to parse date: {publication_date} with error: {e}")
                publication_date = None

        images = json.dumps(item.get('images', []))
        body = json.dumps(item.get('body', []))

        article = Article(
            author=item.get('author'),
            title=item.get('title'),
            publication_date=publication_date,
            url=item.get('url'),
            images=images,
            body=body
        )

        try:
            session.add(article)
            session.commit()
        except Exception as e:
            session.rollback()
            spider.logger.error(f"Failed to add article {item.get('title')} to the database: {e}")
        finally:
            session.close()

        return item