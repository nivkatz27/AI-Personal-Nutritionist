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

# Dependency function to get a database session.
# This function can be used in FastAPI endpoints to provide a database session.
def get_db():
    # Create a new database session for the request.
    db = SessionLocal()
    try:
        # Return the session to the caller without closing it.
        # This allows to close the session after the endpoint function has finished executing.
        yield db
    finally:
        # Close the session to free up resources.
        db.close()
