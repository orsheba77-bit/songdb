import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# בניית URL ממשתני סביבה נפרדים
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

if not all([db_user, db_password, db_host, db_port, db_name]):
    raise ValueError(" Missing required database environment variables!")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# ️ כפיית IPv4 + הגדרות יציבות ל-Render/Supabase
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "options": "-c tcp_keepalives_idle=30 -c tcp_keepalives_interval=10 -c tcp_keepalives_count=5",
        # כפיית IPv4 על ידי שימוש ב-hostaddr במקום host (psycopg2 specific)
    },
    pool_pre_ping=True,  # בדיקת חיבור לפני כל שאילתה
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,  # מחזור חיבורים כל 5 דקות
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()