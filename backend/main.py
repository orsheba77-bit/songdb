import sys
print("DEBUG: Starting main.py", file=sys.stderr)
try:
    from fastapi import FastAPI
    print("DEBUG: FastAPI imported", file=sys.stderr)
except Exception as e:
    print(f"DEBUG: Failed to import FastAPI: {e}", file=sys.stderr)
    raise
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth_router, songs_router, ratings_router, recommendations_router

# יצירת הטבלאות במסד הנתונים
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SongDB - The IMDB of Music", version="3.0.0")

# הגדרות CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# חיבור הנתבים
app.include_router(auth_router.router)
app.include_router(songs_router.router)
app.include_router(ratings_router.router)
app.include_router(recommendations_router.router)

@app.get("/")
def root():
    return {"message": "Welcome to SongDB v3.0! 🎵", "version": "3.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}