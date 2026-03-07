from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Thay PASSWORD và URL bằng Supabase của bạn
DATABASE_URL = "postgresql+psycopg2://postgres.brpcbboulggiqavnvjwl:vmk152200456789@aws-1-ap-south-1.pooler.supabase.com:5432/postgres"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()