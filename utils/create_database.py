from utils.database import Base, engine
from utils.models import Article

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)