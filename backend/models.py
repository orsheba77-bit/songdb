from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ratings = relationship("Rating", back_populates="user", cascade="all, delete-orphan")

class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    spotify_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)
    album = Column(String(255))
    genre = Column(String(100))
    release_year = Column(Integer)
    cover_url = Column(Text)
    preview_url = Column(Text)
    
    # השדה הישראלי שלנו
    is_israeli = Column(Integer, default=0)

    # Audio features
    danceability = Column(Float)
    energy = Column(Float)
    valence = Column(Float)
    tempo = Column(Float)
    acousticness = Column(Float)
    instrumentalness = Column(Float)
    speechiness = Column(Float)
    liveness = Column(Float)

    avg_rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)

    ratings = relationship("Rating", back_populates="song", cascade="all, delete-orphan")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    score = Column(Integer, nullable=False)  # 1-10
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ratings")
    song = relationship("Song", back_populates="ratings")