import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# --------------------------------------------------------------------------
# TODO: PERSISTENCE CONFIGURATION
#
# Docker containers are ephemeral. If we write to "./reviews.db", the data
# is lost when the container restarts.
#
# We have mounted a Docker Volume to the folder '/app/data'.
# You must configure the SQLite URL to store the database file INSIDE that folder.
#
# Format: sqlite:///path/to/file.db
# --------------------------------------------------------------------------
DATABASE_URL = "sqlite:///./reviews.db" # <--- ❌ FIX THIS LINE

# boilerplate configuration
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
