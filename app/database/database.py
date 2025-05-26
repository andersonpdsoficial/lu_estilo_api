from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import time
import sentry_sdk
from sqlalchemy.exc import OperationalError
from app.models.base import Base

load_dotenv()

def get_database():
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123456@db:5432/lu_estilo")
    print(f"Loading DATABASE_URL: {DATABASE_URL}")  # Debug print

    # Validate ASCII characters
    try:
        DATABASE_URL.encode('ascii')
    except UnicodeEncodeError as e:
        error_msg = f"Invalid DATABASE_URL: contains non-ASCII characters - {str(e)}"
        sentry_sdk.capture_message(error_msg)
        raise ValueError(error_msg)

    # Retry mechanism for database connection
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})
            with engine.connect() as conn:
                print("Database connection successful!")
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            return engine, SessionLocal
        except OperationalError as e:
            retry_count += 1
            if retry_count == max_retries:
                error_msg = f"Failed to connect to database after {max_retries} attempts: {str(e)}"
                sentry_sdk.capture_message(error_msg)
                raise
            print(f"Connection attempt {retry_count} failed: {str(e)}. Retrying in 5 seconds...")
            time.sleep(5)

def get_db():
    _, SessionLocal = get_database()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()