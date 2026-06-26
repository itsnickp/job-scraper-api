from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

engine_options = {
    "pool_pre_ping": True,
    "pool_size": 5,
    "max_overflow": 10,
}

if make_url(settings.DATABASE_URL).get_backend_name() == "sqlite":
    engine_options["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, **engine_options)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()
