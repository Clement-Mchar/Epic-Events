from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from models.user import User
from models.client import Client
from models.contract import Contract
from models.event import Event

load_dotenv()

def initialize_database():
    database_url = os.environ.get('DATABASE_URL')

    engine = create_engine(database_url)
    User.metadata.create_all(engine)
    Client.metadata.create_all(engine)
    Contract.metadata.create_all(engine)
    Event.metadata.create_all(engine)

if __name__ == "__main__":
    initialize_database()
