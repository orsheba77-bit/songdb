import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy.orm import Session
from models import Song, Rating

AUDIO_FEATURES = ["danceability", "energy", "valence", "tempo", "acousticness", "instrumentalness", "speechiness", "liveness"]

class RecommendationEngine:

    def get_content_based(self, db: Session, user_id: int, n: int = 10) -> list:
        liked_ratings = db.query(Rating).filter(Rating.user_id == user_id, Rating.score >= 7).all()
        if not liked_ratings:
            return []

        liked_song_ids = [r.song_id for r in liked_ratings]
        liked_songs = db.query(Song).filter(Song.id.in_(liked_song_ids)).all()
        
        all_songs = db.query(Song).filter(Song.danceability.isnot(None)).filter(~Song.id.in_(liked_song_ids)).all()
        if not all_songs:
            return []

        liked_matrix = np.array([[getattr(s, f, 0) or 0 for f in AUDIO_FEATURES] for s in liked_songs])
        all_matrix = np.array([[getattr(s, f, 0) or 0 for f in AUDIO_FEATURES] for s in all_songs])

        # נרמול tempo
        tempo_idx = AUDIO_FEATURES.index("tempo")
        max_tempo = max(all_matrix[:, tempo_idx].max(), 1)
        liked_matrix[:, tempo_idx] /= max_tempo
        all_matrix[:, tempo_idx] /= max_tempo

        sim = cosine_similarity(liked_matrix, all_matrix)
        avg_sim = sim.mean(axis=0)

        top_indices = avg_sim.argsort()[::-1][:n]
        return [{"song": all_songs[idx], "predicted_score": round(float(avg_sim[idx]) * 10, 1), "reason": "content-based"} for idx in top_indices]

    def get_hybrid(self, db: Session, user_id: int, n: int = 10) -> list:
        # בשלב הראשון נשתמש רק ב-Content Based כדי לפשט, בהמשך נוסיף את ה-Collaborative
        return self.get_content_based(db, user_id, n)

engine = RecommendationEngine()