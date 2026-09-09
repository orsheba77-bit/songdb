from .auth_router import router as auth_router
from .songs_router import router as songs_router
from .ratings_router import router as ratings_router
from .recommendations_router import router as recommendations_router

__all__ = ["auth_router", "songs_router", "ratings_router", "recommendations_router"]