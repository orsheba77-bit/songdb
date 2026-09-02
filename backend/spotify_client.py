import httpx
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE = "https://api.spotify.com/v1"

class SpotifyClient:
    def __init__(self):
        self._token = None

    async def _get_token(self) -> str:
        if self._token:
            return self._token
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                TOKEN_URL,
                data={"grant_type": "client_credentials"},
                auth=(CLIENT_ID, CLIENT_SECRET),
            )
            data = resp.json()
            self._token = data["access_token"]
            return self._token

    async def search_tracks(self, query: str, limit: int = 20) -> list:
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{API_BASE}/search",
                params={"q": query, "type": "track", "limit": limit},
                headers={"Authorization": f"Bearer {token}"},
            )
            data = resp.json()
            results = []
            for item in data.get("tracks", {}).get("items", []):
                results.append({
                    "spotify_id": item["id"],
                    "title": item["name"],
                    "artist": ", ".join(a["name"] for a in item["artists"]),
                    "album": item["album"]["name"],
                    "cover_url": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                    "preview_url": item.get("preview_url"),
                })
            return results

    def _detect_israeli_song(self, item: dict) -> bool:
        """מזהה אם שיר הוא ישראלי לפי שם האמן או הז'אנר"""
        israeli_artists = ["עידן רייכל", "עומר אדם", "אייל גולן", "שרית חדד", "דודו אהרון", "משה פרץ", "אברהם טל", "ברי סחרוף", "אביב גפן", "שלומי שבת", "ריטה", "דנה אינטרנשיונל", "מארינה מקסימיליאן", "נסרין קדרי", "סטטיק", "עדן בן זקן", "התקווה 6"]
        
        artist_name = ", ".join(a["name"] for a in item["artists"])
        song_name = item["name"]
        
        # בדיקת תווים בעברית
        def has_hebrew(text):
            return any('\u0590' <= c <= '\u05FF' for c in text)
        
        if has_hebrew(artist_name) or has_hebrew(song_name):
            return True
        
        for israeli_artist in israeli_artists:
            if israeli_artist in artist_name:
                return True
        
        return False

    async def get_track_details(self, spotify_id: str) -> dict:
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{API_BASE}/tracks/{spotify_id}",
                headers={"Authorization": f"Bearer {token}"},
            )
            item = resp.json()
            
            # זיהוי שיר ישראלי
            is_israeli = 1 if self._detect_israeli_song(item) else 0
            
            return {
                "spotify_id": item["id"],
                "title": item["name"],
                "artist": ", ".join(a["name"] for a in item["artists"]),
                "album": item["album"]["name"],
                "release_year": int(item["album"]["release_date"][:4]) if item["album"].get("release_date") else None,
                "cover_url": item["album"]["images"][0]["url"] if item["album"]["images"] else None,
                "preview_url": item.get("preview_url"),
                "is_israeli": is_israeli,
                "danceability": 0.5, # ברירת מחדל, בפרודקשן נמשוך מ-audio-features
                "energy": 0.5,
                "valence": 0.5,
                "tempo": 120.0,
                "acousticness": 0.1,
                "instrumentalness": 0.0,
                "speechiness": 0.05,
                "liveness": 0.1,
            }

spotify_client = SpotifyClient()