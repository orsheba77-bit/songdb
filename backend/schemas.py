from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# --- Auth ---
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str
    password: str = Field(..., min_length=6)

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Songs ---
class SongResponse(BaseModel):
    id: int
    spotify_id: str
    title: str
    artist: str
    album: Optional[str]
    genre: Optional[str]
    release_year: Optional[int]
    cover_url: Optional[str]
    preview_url: Optional[str]
    is_israeli: bool
    avg_rating: float
    total_ratings: int
    class Config:
        from_attributes = True

class SongSearchResult(BaseModel):
    spotify_id: str
    title: str
    artist: str
    album: Optional[str]
    cover_url: Optional[str]
    preview_url: Optional[str]

# --- Ratings ---
class RatingCreate(BaseModel):
    song_id: int
    score: int = Field(..., ge=1, le=10)

class RatingResponse(BaseModel):
    id: int
    user_id: int
    song_id: int
    score: int
    class Config:
        from_attributes = True