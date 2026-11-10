import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

# Local: usa ./moderaai.db. No Docker, o docker-compose define DATABASE_URL
# apontando para o volume persistente (sqlite:////data/moderaai.db).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./moderaai.db")

# connect_args={"check_same_thread": False} é obrigatório para SQLite no FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Gera uma sessão de banco por requisição e fecha ao finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
