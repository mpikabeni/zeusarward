import os
from dotenv import load_dotenv

load_dotenv()

# ==============================
# ZEUS AWARDS - CONFIGURATION
# ==============================

BOT_TOKEN = os.getenv("BOT_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL")

# Environnement
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Fuseau horaire par défaut
TIMEZONE = os.getenv("TIMEZONE", "Africa/Brazzaville")


def validate_config():
    """Vérifie que la configuration minimale est présente."""

    missing = []

    if not BOT_TOKEN:
        missing.append("BOT_TOKEN")

    if not DATABASE_URL:
        missing.append("DATABASE_URL")

    if missing:
        raise RuntimeError(
            "Variables d'environnement manquantes : "
            + ", ".join(missing)
        )


if __name__ == "__main__":
    validate_config()
    print("✅ Configuration ZEUS AWARDS valide.")
