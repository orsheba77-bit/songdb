from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Song, Rating, User
from schemas import RatingCreate, RatingResponse
from auth import get_current_user

router = APIRouter(prefix="/api/ratings", tags=["Ratings"])

@router.post("/", response_model=RatingResponse, status_code=201)
def rate_song(rating: RatingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    song = db.query(Song).filter(Song.id == rating.song_id).first()
    if not song:
        raise HTTPException(404, "Song not found")

    existing = db.query(Rating).filter(Rating.user_id == user.id, Rating.song_id == rating.song_id).first()
    if existing:
        existing.score = rating.score
        db.commit()
        db.refresh(existing)
        return existing

    new_rating = Rating(user_id=user.id, song_id=rating.song_id, score=rating.score)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating