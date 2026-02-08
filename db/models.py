from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Source(Base):
    """Represents a news feed source (RSS feed or API)."""

    __tablename__ = "news_sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, nullable=False)
    section = Column(String, nullable=False, default="")
    source_type = Column(String, nullable=False)  # "rss" or "api"
    url = Column(String, nullable=False, unique=True)
    date_added = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    active = Column(Boolean, default=True)

    subscribers = relationship("UserSubscription", back_populates="source")

    def __repr__(self):
        status = "✓" if self.active else "✗"
        return f"<Source [{status}] {self.source_name} / {self.section} ({self.source_type})>"


class Article(Base):
    """Represents a fetched news article."""

    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date_added = Column(String, nullable=False)  # ISO 8601 timestamp
    last_modified = Column(String, nullable=True)  # ISO 8601 from source
    source = Column(String, nullable=False)
    section_name = Column(String, nullable=True)
    headline = Column(Text, nullable=False)
    web_url = Column(String, nullable=True)
    hash = Column(String(64), nullable=False, unique=True, index=True)

    deliveries = relationship("UserDelivery", back_populates="article")

    def __repr__(self):
        return f"<Article {self.source}: {self.headline[:50]}>"

    def to_dict(self) -> dict:
        """Convert to the standard dict format used throughout the app."""
        return {
            "date_added": self.date_added,
            "lastModified": self.last_modified,
            "source": self.source,
            "sectionName": self.section_name,
            "headline": self.headline,
            "webUrl": self.web_url,
            "hash": self.hash,
        }


class User(Base):
    """Represents a subscriber who receives article emails."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False, default="")
    timezone = Column(String, nullable=False, default="Europe/Berlin")
    delivery_schedule = Column(
        String, nullable=False, default="daily"
    )  # "hourly", "6h", "daily"
    active = Column(Boolean, default=True)
    tier = Column(Integer, nullable=False, default=1)  # 1 = free, 2 = paid
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    subscriptions = relationship("UserSubscription", back_populates="user")
    deliveries = relationship("UserDelivery", back_populates="user")
    tier_changes = relationship("UserTierChange", back_populates="user")
    payments = relationship("UserPayment", back_populates="user")

    def __repr__(self):
        status = "✓" if self.active else "✗"
        return f"<User [{status}] {self.first_name} {self.last_name} ({self.email})>"


class UserSubscription(Base):
    """Links a user to the news sources they want to receive."""

    __tablename__ = "user_subscriptions"
    __table_args__ = (UniqueConstraint("user_id", "source_id", name="uq_user_source"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_id = Column(Integer, ForeignKey("news_sources.id"), nullable=False)
    subscribed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="subscriptions")
    source = relationship("Source", back_populates="subscribers")

    def __repr__(self):
        return f"<Subscription user={self.user_id} source={self.source_id}>"


class UserDelivery(Base):
    """Tracks which articles have been emailed to which user."""

    __tablename__ = "user_deliveries"
    __table_args__ = (
        UniqueConstraint("user_id", "article_id", name="uq_user_article"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    article_id = Column(Integer, ForeignKey("news_articles.id"), nullable=False)
    delivered_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="deliveries")
    article = relationship("Article", back_populates="deliveries")


class LookupTier(Base):
    """Lookup table defining available tier levels."""

    __tablename__ = "lookup_tiers"

    id = Column(Integer, primary_key=True)  # 1, 2, etc.
    tier_name = Column(String, nullable=False, unique=True)  # "free", "subscription"
    date_added = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<LookupTier {self.id}: {self.tier_name}>"


class UserTierChange(Base):
    """Audit log tracking tier changes for each user."""

    __tablename__ = "user_tier_changes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prev_tier = Column(Integer, nullable=True)  # NULL for initial assignment
    new_tier = Column(Integer, nullable=False)
    date_of_change = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="tier_changes")

    def __repr__(self):
        return f"<TierChange user={self.user_id} {self.prev_tier}→{self.new_tier}>"


class UserPayment(Base):
    """Records payments from users, linked to a third-party provider."""

    __tablename__ = "user_payments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    payment_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    payment_amount = Column(String, nullable=False)  # e.g. "2.99"
    payment_currency = Column(String, nullable=False, default="EUR")  # EUR, USD, GBP
    service_provider = Column(String, nullable=False)  # e.g. "stripe", "paypal"
    payment_type = Column(String, nullable=False)  # "one_time" or "subscription"

    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment user={self.user_id} {self.payment_amount} {self.payment_currency} via {self.service_provider}>"
