from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from models.models import User, Client, Contract, Event, Role
from sqlalchemy.orm import sessionmaker

# Load environment variables from a .env file
load_dotenv()

# Get the database URL from environment variables
database_url = os.environ.get('DATABASE_URL')
# Create a SQLAlchemy engine for the specified database URL
engine = create_engine(database_url)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_database():
    # Create tables for all models in the database if they don't exist
    User.metadata.create_all(engine)
    Client.metadata.create_all(engine)
    Contract.metadata.create_all(engine)
    Event.metadata.create_all(engine)
    Role.metadata.create_all(engine)
