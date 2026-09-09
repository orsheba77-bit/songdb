from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import get_current_user
from recommendation_engine import engine

router = APIRouter(prefix="/api/recommendations", tags=["Recommendations"])

@router.get("/")
def get_recommendations(n: int = Query(10, ge=1, le=50), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return engine.get_hybrid(db, user.id, n=n)