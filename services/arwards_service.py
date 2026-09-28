from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from models.models import (
    Award,
    Category,
    Candidate,
    TelegramGroup,
)


# ==========================================
# ZEUS AWARDS - AWARDS SERVICE
# ==========================================


def get_group(
    db: Session,
    telegram_group_id: int,
):
    """Récupère un groupe Telegram."""

    return (
        db.query(TelegramGroup)
        .filter(
            TelegramGroup.telegram_id == telegram_group_id
        )
        .first()
    )


def create_award(
    db: Session,
    telegram_group_id: int,
    name: str,
    description: str | None = None,
):
    """Crée une nouvelle cérémonie."""

    group = get_group(
        db,
        telegram_group_id,
    )

    if not group:
        raise ValueError(
            "Ce groupe n'est pas encore enregistré."
        )

    award = Award(
        group_id=group.id,
        name=name,
        description=description,
        status="draft",
    )

    db.add(award)
    db.commit()
    db.refresh(award)

    return award


def add_category(
    db: Session,
    award_id: int,
    name: str,
    description: str | None = None,
):
    """Ajoute une catégorie à une cérémonie."""

    award = (
        db.query(Award)
        .filter(Award.id == award_id)
        .first()
    )

    if not award:
        raise ValueError(
            "Cérémonie introuvable."
        )

    category = Category(
        award_id=award.id,
        name=name,
        description=description,
        max_votes_per_user=1,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def add_candidate(
    db: Session,
    category_id: int,
    name: str,
    anime_name: str | None = None,
    description: str | None = None,
    image_url: str | None = None,
):
    """Ajoute un candidat."""

    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise ValueError(
            "Catégorie introuvable."
        )

    candidate = Candidate(
        category_id=category.id,
        name=name,
        anime_name=anime_name,
        description=description,
        image_url=image_url,
    )

    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    return candidate


def start_award(
    db: Session,
    award_id: int,
    duration_minutes: int,
):
    """Ouvre les votes d'une cérémonie."""

    award = (
        db.query(Award)
        .filter(Award.id == award_id)
        .first()
    )

    if not award:
        raise ValueError(
            "Cérémonie introuvable."
        )

    if not award.categories:
        raise ValueError(
            "La cérémonie doit avoir au moins une catégorie."
        )

    for category in award.categories:

        if not category.candidates:
            raise ValueError(
                f"La catégorie '{category.name}' "
                "ne possède aucun candidat."
            )

    now = datetime.utcnow()

    award.status = "voting"
    award.voting_started_at = now
    award.voting_ends_at = (
        now + timedelta(minutes=duration_minutes)
    )

    db.commit()
    db.refresh(award)

    return award


def close_award(
    db: Session,
    award_id: int,
):
    """Ferme les votes."""

    award = (
        db.query(Award)
        .filter(Award.id == award_id)
        .first()
    )

    if not award:
        raise ValueError(
            "Cérémonie introuvable."
        )

    award.status = "closed"

    db.commit()
    db.refresh(award)

    return award


def get_active_awards(
    db: Session,
    telegram_group_id: int,
):
    """Retourne les cérémonies actives d'un groupe."""

    group = get_group(
        db,
        telegram_group_id,
    )

    if not group:
        return []

    return (
        db.query(Award)
        .filter(
            Award.group_id == group.id,
            Award.status == "voting",
        )
        .all()
    )


def get_award(
    db: Session,
    award_id: int,
):
    """Récupère une cérémonie."""

    return (
        db.query(Award)
        .filter(Award.id == award_id)
        .first()
    )
