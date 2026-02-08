"""
Migrates existing articles from CSV into the articles table.
Run once:  python -m db.migrate_csv

Safe to re-run — skips articles whose hash already exists in the DB.
"""

import logging
import os

import pandas as pd

from db import engine, get_session
from db.models import Article, Base

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

CSV_FILE = "articles.csv"


def migrate():
    """Reads articles.csv and inserts rows into the articles table."""
    Base.metadata.create_all(engine)

    if not os.path.exists(CSV_FILE):
        logger.warning(f"{CSV_FILE} not found. Nothing to migrate.")
        return

    df = pd.read_csv(CSV_FILE)
    logger.info(f"Read {len(df)} rows from {CSV_FILE}.")

    session = get_session()
    added = 0
    skipped = 0

    try:
        existing_hashes = {row.hash for row in session.query(Article.hash).all()}

        for _, row in df.iterrows():
            h = str(row.get("hash", ""))
            if h in existing_hashes:
                skipped += 1
                continue

            article = Article(
                date_added=str(row.get("date_added", "")),
                last_modified=str(row.get("lastModified", "")),
                source=str(row.get("source", "")),
                section_name=str(row.get("sectionName", "")),
                headline=str(row.get("headline", "")),
                web_url=str(row.get("webUrl", "")),
                hash=h,
            )
            session.add(article)
            added += 1

        session.commit()
        logger.info(
            f"Migration complete: {added} added, {skipped} skipped (already exist)."
        )
    except Exception as e:
        session.rollback()
        logger.error(f"Migration failed: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    migrate()
