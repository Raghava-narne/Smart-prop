from app.core.config import settings
from app.db.session import SessionLocal, engine

DATABASE_URL = settings.database_url