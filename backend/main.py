import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base

print("✅ Starting main.py", file=sys.stderr)

# ייבוא ישיר של כל ראוטר עם הדפסה בין לבין
try:
    from routers.auth_router import router as auth_router
    print("✅ Auth router imported", file=sys.stderr)
except Exception as e:
    print(f"❌ Failed to import auth_router: {e}", file=sys.stderr)
    raise

try:
    from routers.songs_router import router as songs_router
    print("✅ Songs router imported", file=sys.stderr)
except Exception as e:
    print(f"❌ Failed to import songs_router: {e}", file=sys.stderr)
    raise

try:
    from routers.ratings_router import router as ratings_router
    print("✅ Ratings router imported", file=sys.stderr)
except Exception as e:
    print(f" Failed to import ratings_router: {e}", file=sys.stderr)
    raise

try:
    from routers.recommendations_router import router as recommendations_router
    print("✅ Recommendations router imported", file=sys.stderr)
except Exception as e:
    print(f" Failed to import recommendations_router: {e}", file=sys.stderr)
    raise

# יצירת הטבלאות במסד הנתונים
print(" Creating database tables...", file=sys.stderr)
print("✅ Database tables created", file=sys.stderr)

# יצירת האפליקציה
app = FastAPI(title="SongDB - The IMDB of Music", version="3.0.0")
print("✅ App created", file=sys.stderr)

# הגדרות CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("✅ CORS configured", file=sys.stderr)

# חיבור הנתבים (שים לב: אנחנו מוסיפים את 'router' כי ייבאנו אותו כ-'auth_router')
app.include_router(auth_router)
app.include_router(songs_router)
app.include_router(ratings_router)
app.include_router(recommendations_router)
print("✅ All routers included", file=sys.stderr)

@app.get("/")
def root():
    return {"message": "Welcome to SongDB v3.0! 🎵", "version": "3.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

print("🚀 Server startup complete!", file=sys.stderr)