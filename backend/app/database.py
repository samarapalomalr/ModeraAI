from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./moderaai.db"

# connect_args={"check_same_thread": False} é obrigatório para SQLite no FastAPI
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Gera uma sessão de banco por requisição e fecha ao finalizar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
