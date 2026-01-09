"""
Database base configuration and session management.
"""
from typing import Generator, Optional

try:
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    print("⚠️  SQLAlchemy not available - database features disabled")
    print("   Mock data mode will still work!")

from backend.config import settings

# Create Base class for models (if SQLAlchemy available)
Base = declarative_base() if SQLALCHEMY_AVAILABLE else None

# Lazy initialization
engine = None
SessionLocal = None

if SQLALCHEMY_AVAILABLE:
    try:
        # Create SQLAlchemy engine
        engine = create_engine(
            settings.database_url,
            pool_size=settings.database_pool_size,
            max_overflow=settings.database_max_overflow,
            echo=settings.debug,
            connect_args={'connect_timeout': 3}  # Fast timeout for mock mode
        )
        # Create SessionLocal class
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   Running without database (mock mode only)")
        engine = None
        SessionLocal = None


def get_db() -> Generator[Optional[object], None, None]:
    """
    Dependency function to get database session.
    Returns None if database is not available (mock mode).
    """
    if SessionLocal is None:
        yield None
        return

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database, create all tables."""
    if engine is None or Base is None:
        print("⚠️  Database not available - skipping initialization")
        return
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization failed: {e}")


def drop_db() -> None:
    """Drop all tables (use with caution!)."""
    if engine is None or Base is None:
        print("⚠️  Database not available")
        return
    Base.metadata.drop_all(bind=engine)
