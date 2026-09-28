from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DATABASE_URL


# ==============================
# ZEUS AWARDS - DATABASE
# ==============================

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL n'est pas configurée dans les variables d'environnement."
    )


# Render peut fournir une URL PostgreSQL commençant par postgres://
# SQLAlchemy utilise postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql://",
        1
    )


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    pass


def get_db():
    """
    Crée une session PostgreSQL.
    La session est automatiquement fermée après utilisation.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def init_database():
    """
    Crée toutes les tables déclarées dans les modèles.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ Base de données ZEUS AWARDS initialisée.")
