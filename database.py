from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from models.models import User, Client, Contract, Event, Role
from sqlalchemy.orm import sessionmaker

load_dotenv()

database_url = os.environ.get('DATABASE_URL')

engine = create_engine(database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():

    User.metadata.create_all(engine)
    Client.metadata.create_all(engine)
    Contract.metadata.create_all(engine)
    Event.metadata.create_all(engine)
    Role.metadata.create_all(engine)

''' 
 id | code |    name
----+------+------------
  1 | man  | Manager
  2 | com  | Commercial
  3 | sup  | Support '''