from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import Song
from schemas import SongResponse, SongSearchResult
from spotify_client import spotify_client

router = APIRouter(prefix="/api/songs", tags=["Songs"])

@router.get("/search", response_model=list[SongSearchResult])
async def search(q: str = Query(..., min_length=2)):
    return await spotify_client.search_tracks(q)

@router.get("/top", response_model=list[SongResponse])
def top_rated(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return db.query(Song).filter(Song.total_ratings > 0).order_by(Song.avg_rating.desc()).limit(limit).all()

@router.get("/israeli/top", response_model=list[SongResponse])
def top_israeli(limit: int = Query(20, ge=1, le=100), db: Session = Depends(get_db)):
    return db.query(Song).filter(Song.is_israeli == 1, Song.total_ratings > 0).order_by(Song.avg_rating.desc()).limit(limit).all()