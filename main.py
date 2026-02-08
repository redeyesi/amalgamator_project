import os
import logging
from datetime import datetime

from dotenv import load_dotenv

from sources import guardian, rss
from utils.dedup import deduplicate
from utils.storage import load_existing_hashes, save_articles
from utils.email_service import send_email_for_user
from db import get_session
from db.models import Article, Source, User, UserDelivery, UserSubscription


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


# --- Fetch Layer (shared, source-driven) ---


def fetch_all_sources(logger) -> None:
    """
    Fetches articles from every active source, deduplicates against the
    global articles table, and saves new articles.  This is user-agnostic.
    """
    load_dotenv()

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
        logger.info("No articles returned from any source.")
        return

    # --- Deduplicate & save globally ---
    existing_hashes = load_existing_hashes()
    new_rows = deduplicate(all_articles, existing_hashes)

    if new_rows:
        save_articles(new_rows)
    else:
        logger.info("No new articles found after deduplication.")


# --- Delivery Layer (per-user) ---


def deliver_to_users(logger) -> None:
    """
    For each active user, finds articles from their subscribed sources
    that haven't been delivered yet, sends an email, and records the delivery.
    """
    EMAIL_SENDER = "datacollectionstorage@gmail.com"
    session = get_session()

    try:
        active_users = session.query(User).filter(User.active == True).all()
        logger.info(f"Processing deliveries for {len(active_users)} active user(s).")

        for user in active_users:
            # Get this user's subscribed source names
            subscribed_source_ids = {
                sub.source_id
                for sub in session.query(UserSubscription)
                .filter(UserSubscription.user_id == user.id)
                .all()
            }

            if not subscribed_source_ids:
                logger.info(f"User {user.email} has no subscriptions. Skipping.")
                continue

            # Get source names for subscribed IDs
            subscribed_sources = (
                session.query(Source).filter(Source.id.in_(subscribed_source_ids)).all()
            )
            source_names = {s.source_name for s in subscribed_sources}

            # Get article IDs already delivered to this user
            delivered_article_ids = {
                row.article_id
                for row in session.query(UserDelivery.article_id)
                .filter(UserDelivery.user_id == user.id)
                .all()
            }

            # Find undelivered articles from subscribed sources
            query = session.query(Article).filter(
                Article.source.in_(source_names),
            )
            if delivered_article_ids:
                query = query.filter(Article.id.notin_(delivered_article_ids))

            pending_articles = query.order_by(Article.id.desc()).all()

            if not pending_articles:
                logger.info(f"No new articles for {user.email}.")
                continue

            # Convert to dicts for the email renderer
            article_dicts = [a.to_dict() for a in pending_articles]

            logger.info(f"Delivering {len(article_dicts)} articles to {user.email}.")

            # Send email
            send_email_for_user(
                articles=article_dicts,
                sender=EMAIL_SENDER,
                recipient=user.email,
                user_name=f"{user.first_name} {user.last_name}".strip(),
                user_timezone=user.timezone,
            )

            # Record deliveries
            for article in pending_articles:
                session.add(UserDelivery(user_id=user.id, article_id=article.id))
            session.commit()
            logger.info(
                f"Recorded {len(pending_articles)} deliveries for {user.email}."
            )

    except Exception as e:
        session.rollback()
        logger.error(f"Delivery failed: {e}")
        raise
    finally:
        session.close()


# --- Main Orchestrator ---


def main():
    """
    Main entry point.
    Step 1: Fetch articles from all active sources (shared).
    Step 2: Deliver new articles to each subscribed user (per-user).
    """
    logger = setup_logging()

    logger.info("=== STEP 1: Fetching articles ===")
    fetch_all_sources(logger)

    logger.info("=== STEP 2: Delivering to users ===")
    deliver_to_users(logger)

    logger.info("Process completed.")


if __name__ == "__main__":
    main()
