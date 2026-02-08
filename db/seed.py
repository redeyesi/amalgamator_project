"""
Seeds the database with news sources and the default user.
Run once:  python -m db.seed
Re-run is safe — skips records that already exist.
"""

import logging

from db import engine, get_session
from db.models import Base, LookupTier, Source, User, UserSubscription, UserTierChange

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# fmt: off
SEED_SOURCES = [
    # ── Currently active ─────────────────────────────────────────────
    # Guardian API
    {"source_name": "The Guardian",       "section": "World",          "source_type": "api", "url": "https://content.guardianapis.com/search",                          "active": True},

    # RSS — World News
    {"source_name": "BBC News",           "section": "World",          "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/world/rss.xml",                      "active": True},
    {"source_name": "BBC News",           "section": "UK",             "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/uk/rss.xml",                         "active": True},
    {"source_name": "Al Jazeera",         "section": "All",            "source_type": "rss", "url": "https://www.aljazeera.com/xml/rss/all.xml",                        "active": True},
    {"source_name": "NPR",                "section": "News",           "source_type": "rss", "url": "https://feeds.npr.org/1001/rss.xml",                               "active": True},

    # ── Available but inactive ───────────────────────────────────────
    # World News
    {"source_name": "The Guardian",       "section": "World",          "source_type": "rss", "url": "https://www.theguardian.com/world/rss",                            "active": False},
    {"source_name": "France 24",          "section": "World",          "source_type": "rss", "url": "https://www.france24.com/en/rss",                                  "active": False},
    {"source_name": "DW",                 "section": "World",          "source_type": "rss", "url": "https://rss.dw.com/rdf/rss-en-all",                                "active": False},

    # Technology
    {"source_name": "BBC News",           "section": "Technology",     "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/technology/rss.xml",                 "active": False},
    {"source_name": "Hacker News",        "section": "Technology",     "source_type": "rss", "url": "https://hnrss.org/frontpage",                                      "active": False},
    {"source_name": "The Verge",          "section": "Technology",     "source_type": "rss", "url": "https://www.theverge.com/rss/index.xml",                           "active": False},
    {"source_name": "Ars Technica",       "section": "Technology",     "source_type": "rss", "url": "https://feeds.arstechnica.com/arstechnica/index",                  "active": False},
    {"source_name": "TechCrunch",         "section": "Technology",     "source_type": "rss", "url": "https://techcrunch.com/feed/",                                     "active": False},
    {"source_name": "Wired",              "section": "Technology",     "source_type": "rss", "url": "https://www.wired.com/feed/rss",                                   "active": False},
    {"source_name": "The Register",       "section": "Technology",     "source_type": "rss", "url": "https://www.theregister.com/headlines.atom",                       "active": False},

    # Science & Environment
    {"source_name": "BBC News",           "section": "Science",        "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",    "active": False},
    {"source_name": "Nature",             "section": "Science",        "source_type": "rss", "url": "https://www.nature.com/nature.rss",                                "active": False},
    {"source_name": "NASA",               "section": "Breaking News",  "source_type": "rss", "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",                  "active": False},

    # Business & Finance
    {"source_name": "BBC News",           "section": "Business",       "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/business/rss.xml",                   "active": False},

    # Sport
    {"source_name": "BBC Sport",          "section": "Sport",          "source_type": "rss", "url": "https://feeds.bbci.co.uk/sport/rss.xml",                           "active": False},
    {"source_name": "ESPN",               "section": "Top Headlines",  "source_type": "rss", "url": "https://www.espn.com/espn/rss/news",                               "active": False},

    # Entertainment & Culture
    {"source_name": "BBC News",           "section": "Entertainment",  "source_type": "rss", "url": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",     "active": False},
    {"source_name": "The Guardian",       "section": "Culture",        "source_type": "rss", "url": "https://www.theguardian.com/uk/culture/rss",                       "active": False},
]
# fmt: on


def seed():
    """Creates the tables and inserts seed data (skips existing records)."""
    Base.metadata.create_all(engine)
    session = get_session()

    added = 0
    skipped = 0

    try:
        # --- Seed news sources ---
        existing_urls = {row.url for row in session.query(Source.url).all()}

        for data in SEED_SOURCES:
            if data["url"] in existing_urls:
                skipped += 1
                continue
            session.add(Source(**data))
            added += 1

        session.commit()
        logger.info(f"Sources: {added} added, {skipped} already existed.")

        # --- Seed lookup tiers ---
        existing_tier_ids = {row.id for row in session.query(LookupTier.id).all()}
        tier_added = 0
        for tier_data in [
            {"id": 1, "tier_name": "free"},
            {"id": 2, "tier_name": "subscription"},
        ]:
            if tier_data["id"] not in existing_tier_ids:
                session.add(LookupTier(**tier_data))
                tier_added += 1
        session.commit()
        logger.info(f"Tiers: {tier_added} added, {2 - tier_added} already existed.")

        # --- Seed default user ---
        default_email = "simongreen1@gmail.com"
        user = session.query(User).filter(User.email == default_email).first()
        if not user:
            user = User(
                email=default_email,
                first_name="Simon",
                last_name="Green",
                timezone="Europe/Berlin",
                delivery_schedule="daily",
                tier=1,
                active=True,
            )
            session.add(user)
            session.commit()
            # Record initial tier assignment
            session.add(UserTierChange(user_id=user.id, prev_tier=None, new_tier=1))
            session.commit()
            logger.info(f"Created default user: {user.email}")
        else:
            logger.info(f"Default user already exists: {user.email}")

        # --- Subscribe default user to all active sources ---
        active_sources = session.query(Source).filter(Source.active == True).all()
        existing_subs = {
            row.source_id
            for row in session.query(UserSubscription.source_id)
            .filter(UserSubscription.user_id == user.id)
            .all()
        }

        sub_added = 0
        for source in active_sources:
            if source.id not in existing_subs:
                session.add(UserSubscription(user_id=user.id, source_id=source.id))
                sub_added += 1

        session.commit()
        logger.info(
            f"Subscriptions: {sub_added} added, "
            f"{len(active_sources) - sub_added} already existed."
        )

    except Exception as e:
        session.rollback()
        logger.error(f"Seed failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
