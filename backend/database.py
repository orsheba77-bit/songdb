import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# בניית URL ממשתני סביבה נפרדים כדי להימנע מבעיות קידוד
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# בדיקה שכל המשתנים קיימים לפני יצירת ה-Engine
if not all([db_user, db_password, db_host, db_port, db_name]):
    raise ValueError("❌ Missing required database environment variables! Check Render settings.")

DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# יצירת Engine ו-Base
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# פונקציית Helper לקבלת Session (אם הייתה לך כזו בקוד המקורי)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()