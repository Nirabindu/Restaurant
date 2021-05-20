from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHAMY_DATABASE_URL = "mysql+mysqlconnector://root:admin@localhost:3306/restaurant"
# SQLALCHAMY_DATABASE_URL = "mysql+mysqlconnector://eatify:eatify1234@host:eatify-db.cpezwwmmqd57.ap-south-1.rds.amazonaws.com:3306/restuarant"
# SQLALCHAMY_DATABASE_URL = "mysql+mysqlconnector://restaurant:restaurant_1234@database-nirabindu.cpezwwmmqd57.ap-south-1.rds.amazonaws.com:3306/restaurant"

 
engine = create_engine(SQLALCHAMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False,autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   