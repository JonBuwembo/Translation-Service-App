import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

#uvicorn app.main:app --reload :To run the app

# To keep our variables that contain sensitive data safe, import this.
from dotenv import load_dotenv

# loads environment variables from .env file into system's environment variables.
# useful in dev environments where you may not want to hard code sensitive info, such as db credentials
load_dotenv() 

# line retrieves the database URL in .env file.
# Environment variables: often used to keep sensitive information safe and out of source code.
# keeps data secure and configurable across different environments (development, testing, production)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") # How you keep your stored data safe 

# core interface of database --> handles connection pool and other database-specific details.
# provides necessary connection details for the database
# used to manage the actual database connection and execute SQL statements.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Sessionmaker(): "session factory" used to create new session objects
# This factory will be used to creature new session objects
# these objects reponsible for managing queries and transactions against the database.
# AUTOCOMMIT=FALSE: indicates that the session will not automatically commit transactions, you will explicitly commit them.
# AUTOFLUSH=FALSE: means that session will not automatically flush (synchronize) changes to the database before executing queries.
# BIND=ENGINE: associates the created sessions with previously created engine --> so they use the same db connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


if not database_exists(engine.url):
    create_database(engine.url)
    print("Database created.")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



