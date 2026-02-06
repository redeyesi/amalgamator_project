import os
import logging
from datetime import datetime

from dotenv import load_dotenv

from sources import guardian, rss
from utils.dedup import deduplicate
from utils.storage import load_existing_hashes, save_articles
from utils.email_service import send_email


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

    # --- Fetch from all sources ---
    all_articles = []

    # Guardian
    guardian_key = os.getenv("GUARDIAN_API_KEY")
    if guardian_key:
        all_articles.extend(guardian.fetch(guardian_key))
    else:
        logger.warning("GUARDIAN_API_KEY not set. Skipping Guardian.")

    # --- RSS Feeds ---
    rss_feeds = [
        {
            "feed_url": "https://feeds.bbci.co.uk/news/world/rss.xml",
            "source_name": "BBC News",
            "section": "World",
        },
        {
            "feed_url": "https://feeds.bbci.co.uk/news/uk/rss.xml",
            "source_name": "BBC News",
            "section": "UK",
        },
        {
            "feed_url": "https://www.aljazeera.com/xml/rss/all.xml",
            "source_name": "Al Jazeera",
        },
        {
            "feed_url": "https://feeds.npr.org/1001/rss.xml",
            "source_name": "NPR",
            "section": "News",
        },
        {
            "feed_url": "https://rsshub.app/apnews/topics/apf-topnews",
            "source_name": "Associated Press",
            "section": "Top News",
        },
    ]

    for feed in rss_feeds:
        all_articles.extend(rss.fetch(**feed, max_items=5))

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
