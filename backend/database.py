import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from the .env file.
load_dotenv()

# Load the database connection URL from the environment.
DATABASE_URL = os.environ["DATABASE_URL"]

# Create SQLAlchemy's connection manager for PostgreSQL.
engine = create_engine(DATABASE_URL)

# Create a factory for database sessions.
# every time you call SessionLocal(), it will create a new session connected to the database.
SessionLocal = sessionmaker(bind=engine)


