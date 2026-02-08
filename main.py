import os
import logging
from datetime import datetime

from dotenv import load_dotenv

from sources import guardian, rss
from utils.dedup import deduplicate
from utils.storage import load_existing_hashes, save_articles
from utils.email_service import send_email
from db import get_session
from db.models import Source


# --- Configuration & Logging Setup ---


def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """
    Sets up logging to both file and console.
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_filename = os.path.join(log_dir, f"amalgamator-{log_timestamp}.log")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_filename, mode="a"),
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(__name__)


# --- Main Orchestrator ---


def main():
    """
    Main entry point. Fetches articles from all sources, deduplicates,
    saves to CSV, and sends an email notification.
    """
    logger = setup_logging()
    load_dotenv()

    CSV_FILE = "articles.csv"
    EMAIL_SENDER = "datacollectionstorage@gmail.com"
    EMAIL_RECIPIENTS = ["simongreen1@gmail.com"]

    # --- Fetch from all active sources ---
    all_articles = []
    session = get_session()

    try:
        active_sources = session.query(Source).filter(Source.active == True).all()
        logger.info(f"Loaded {len(active_sources)} active sources from database.")

        for source in active_sources:
            if source.source_type == "api" and "guardianapis" in source.url:
                guardian_key = os.getenv("GUARDIAN_API_KEY")
                if guardian_key:
                    all_articles.extend(guardian.fetch(guardian_key))
                else:
                    logger.warning("GUARDIAN_API_KEY not set. Skipping Guardian.")

            elif source.source_type == "rss":
                all_articles.extend(
                    rss.fetch(
                        feed_url=source.url,
                        source_name=source.source_name,
                        section=source.section,
                        max_items=5,
                    )
                )
    finally:
        session.close()

    if not all_articles:
        logger.info("No articles returned from any source. Exiting.")
        return

    # --- Deduplicate ---
    existing_hashes = load_existing_hashes(CSV_FILE)
    new_rows = deduplicate(all_articles, existing_hashes)

    if new_rows:
        save_articles(new_rows, CSV_FILE)
        send_email(new_rows, EMAIL_SENDER, EMAIL_RECIPIENTS)
    else:
        logger.info("No new articles found after deduplication.")

    logger.info("Process completed.")


if __name__ == "__main__":
    main()
