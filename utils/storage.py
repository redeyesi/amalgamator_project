import logging
from typing import List, Dict, Any, Set

from db import get_session
from db.models import Article

logger = logging.getLogger(__name__)


def load_existing_hashes() -> Set[str]:
    """
    Loads existing article hashes from the database to prevent duplicates.
    """
    session = get_session()
    try:
        hashes = {row.hash for row in session.query(Article.hash).all()}
        logger.info(f"Loaded {len(hashes)} existing article hashes from database.")
        return hashes
    except Exception as e:
        logger.error(f"Error reading existing hashes: {e}")
        return set()
    finally:
        session.close()


def save_articles(new_rows: List[Dict[str, Any]]) -> None:
    """
    Saves new articles to the database.
    """
    if not new_rows:
        logger.info("No new rows to save.")
        return

    session = get_session()
    try:
        for row in new_rows:
            article = Article(
                date_added=row.get("date_added", ""),
                last_modified=row.get("lastModified", ""),
                source=row.get("source", ""),
                section_name=row.get("sectionName", ""),
                headline=row.get("headline", ""),
                web_url=row.get("webUrl", ""),
                hash=row.get("hash", ""),
            )
            session.add(article)

        session.commit()
        logger.info(f"Successfully saved {len(new_rows)} articles to database.")
    except Exception as e:
        session.rollback()
        logger.error(f"Failed to save articles: {e}")
    finally:
        session.close()
