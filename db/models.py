from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Source(Base):
    """Represents a news feed source (RSS feed or API)."""

    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_name = Column(String, nullable=False)
    section = Column(String, nullable=False, default="")
    source_type = Column(String, nullable=False)  # "rss" or "api"
    url = Column(String, nullable=False, unique=True)
    date_added = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    active = Column(Boolean, default=True)

    def __repr__(self):
        status = "✓" if self.active else "✗"
        return f"<Source [{status}] {self.source_name} / {self.section} ({self.source_type})>"
