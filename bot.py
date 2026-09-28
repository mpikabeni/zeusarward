import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, validate_config
from database import SessionLocal, init_database
from models.models import User, TelegramGroup


# ==========================================
# ZEUS AWARDS - BOT PRINCIPAL
# ==========================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("ZEUS_AWARDS")


# ==========================================
# ENREGISTREMENT UTILISATEUR
# ==========================================

def register_user(update: Update):
    """Enregistre ou met à jour un utilisateur."""

    if not update.effective_user:
        return

    telegram_user = update.effective_user

    db = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(
                User.telegram_id == telegram_user.id
            )
            .first()
        )

        if user is None:
            user = User(
                telegram_id=telegram_user.id,
                username=telegram_user.username,
                first_name=telegram_user.first_name,
                last_name=telegram_user.last_name,
            )

            db.add(user)

        else:
            user.username = telegram_user.username
            user.first_name = telegram_user.first_name
            user.last_name = telegram_user.last_name

        db.commit()

    except Exception:
        db.rollback()
        logger.exception(
            "Erreur lors de l'enregistrement de l'utilisateur."
        )

    finally:
        db.close()


# ==========================================
# ENREGISTREMENT GROUPE
# ==========================================

def register_group(update: Update):
    """Enregistre automatiquement le groupe."""

    if not update.effective_chat:
        return

    chat = update.effective_chat

    if chat.type not in ("group", "supergroup"):
        return

    db = SessionLocal()

    try:
        group = (
            db.query(TelegramGroup)
            .filter(
                TelegramGroup.telegram_id == chat.id
            )
            .first()
        )

        if group is None:
            group = TelegramGroup(
                telegram_id=chat.id,
                title=chat.title or "Groupe sans nom",
                username=chat.username,
            )

            db.add(group)

        else:
            group.title = chat.title or group.title
            group.username = chat.username

        db.commit()

    except Exception:
        db.rollback()
        logger.exception(
            "Erreur lors de l'enregistrement du groupe."
        )

    finally:
        db.close()


# ==========================================
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    register_user(update)
    register_group(update)

    if update.effective_chat.type in (
        "group",
        "supergroup",
    ):

        await update.message.reply_text(
            "⚡ ZEUS AWARDS est maintenant actif dans ce groupe !\n\n"
            "🏆 Des Awards anime\n"
            "🗳️ Des votes\n"
            "🎴 Des catégories\n"
            "🎤 Des cérémonies\n"
            "🏅 Des classements\n\n"
            "Utilisez /awards pour découvrir les Awards disponibles."
        )

    else:

        await update.message.reply_text(
            "⚡ Bienvenue sur ZEUS AWARDS !\n\n"
            "🏆 Le bot communautaire dédié aux Awards anime.\n\n"
            "🎴 Participe aux cérémonies\n"
            "🗳️ Vote pour tes favoris\n"
            "🏅 Gagne des badges\n"
            "📊 Consulte tes statistiques\n\n"
            "Utilise /awards pour commencer."
        )


# ==========================================
# MESSAGE DE TEST
# ==========================================

async def awards(update: Update, context: ContextTypes.DEFAULT_TYPE):

    register_user(update)
    register_group(update)

    await update.message.reply_text(
        "🏆 ZEUS AWARDS\n\n"
        "Aucun Award actif pour le moment.\n\n"
        "⚡ Les prochaines cérémonies seront affichées ici."
    )


# ==========================================
# ERREURS
# ==========================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):

    logger.error(
        "Erreur Telegram : %s",
        context.error,
        exc_info=context.error,
    )


# ==========================================
# DÉMARRAGE
# ==========================================

def main():

    validate_config()

    init_database()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("awards", awards)
    )

    application.add_error_handler(
        error_handler
    )

    logger.info(
        "⚡ ZEUS AWARDS démarre..."
    )

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
