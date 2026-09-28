from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


# ==========================================
# UTILISATEURS
# ==========================================

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    first_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    last_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    votes = relationship(
        "Vote",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    badges = relationship(
        "UserBadge",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# ==========================================
# GROUPES TELEGRAM
# ==========================================

class TelegramGroup(Base):
    __tablename__ = "telegram_groups"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    username: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    awards = relationship(
        "Award",
        back_populates="group",
        cascade="all, delete-orphan",
    )


# ==========================================
# AWARDS / CÉRÉMONIES
# ==========================================

class Award(Base):
    __tablename__ = "awards"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_groups.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="draft",
        nullable=False,
    )

    voting_started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    voting_ends_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    group = relationship(
        "TelegramGroup",
        back_populates="awards",
    )

    categories = relationship(
        "Category",
        back_populates="award",
        cascade="all, delete-orphan",
    )


# ==========================================
# CATÉGORIES
# ==========================================

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    award_id: Mapped[int] = mapped_column(
        ForeignKey("awards.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    max_votes_per_user: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    award = relationship(
        "Award",
        back_populates="categories",
    )

    candidates = relationship(
        "Candidate",
        back_populates="category",
        cascade="all, delete-orphan",
    )

    votes = relationship(
        "Vote",
        back_populates="category",
        cascade="all, delete-orphan",
    )


# ==========================================
# CANDIDATS
# ==========================================

class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    anime_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    category = relationship(
        "Category",
        back_populates="candidates",
    )

    votes = relationship(
        "Vote",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )


# ==========================================
# VOTES
# ==========================================

class Vote(Base):
    __tablename__ = "votes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("candidates.id"),
        nullable=False,
        index=True,
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("telegram_groups.id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="votes",
    )

    category = relationship(
        "Category",
        back_populates="votes",
    )

    candidate = relationship(
        "Candidate",
        back_populates="votes",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "category_id",
            "group_id",
            name="unique_user_category_group_vote",
        ),
    )


# ==========================================
# BADGES
# ==========================================

class Badge(Base):
    __tablename__ = "badges"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    icon: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    user_badges = relationship(
        "UserBadge",
        back_populates="badge",
        cascade="all, delete-orphan",
    )


# ==========================================
# BADGES DES UTILISATEURS
# ==========================================

class UserBadge(Base):
    __tablename__ = "user_badges"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    badge_id: Mapped[int] = mapped_column(
        ForeignKey("badges.id"),
        nullable=False,
        index=True,
    )

    earned_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="badges",
    )

    badge = relationship(
        "Badge",
        back_populates="user_badges",
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "badge_id",
            name="unique_user_badge",
        ),
    )
