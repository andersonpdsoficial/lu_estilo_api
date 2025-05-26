from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:628629@localhost:5432/lu_estilo")
print(f"Using DATABASE_URL: {DATABASE_URL}")
try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {str(e)}")