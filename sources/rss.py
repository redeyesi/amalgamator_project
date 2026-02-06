import logging
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import List, Dict, Any, Optional

import feedparser

logger = logging.getLogger(__name__)


def _normalise_date(raw_date: str) -> str:
    """
    Converts RFC 2822 dates (common in RSS) to ISO 8601 format
    so downstream code only needs to handle one format.
    Returns the original string if parsing fails.
    """
    if not raw_date:
        return raw_date
    try:
        dt = parsedate_to_datetime(raw_date)  # RFC 2822 → datetime
        return dt.astimezone(timezone.utc).isoformat()  # → ISO 8601 with +00:00
    except Exception:
        return raw_date  # already ISO or unparseable — pass through


def fetch(
    feed_url: str,
    source_name: str,
    section: str = "",
    max_items: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Fetches articles from any RSS/Atom feed and returns them in
    the standardised article format.

    Args:
        feed_url:    Full URL of the RSS/Atom feed.
        source_name: Human-readable name (e.g. "BBC News").
        section:     Section label to attach (e.g. "Technology").
        max_items:   Optional cap on number of articles returned.
    """
    logger.debug(f"Fetching RSS feed: {feed_url}")

    try:
        feed = feedparser.parse(feed_url)
    except Exception as e:
        logger.error(f"RSS fetch failed for {feed_url}: {e}")
        return []

    if feed.bozo and feed.bozo_exception:
        logger.warning(f"RSS parse warning for {feed_url}: {feed.bozo_exception}")

    entries = feed.entries
    if max_items:
        entries = entries[:max_items]

    articles = []
    for entry in entries:
        # Use 'published' first, fall back to 'updated', then empty
        last_modified = _normalise_date(
            entry.get("published", entry.get("updated", ""))
        )

        # Some feeds provide tags/categories we can use as section
        entry_section = section
        if not entry_section and entry.get("tags"):
            entry_section = entry["tags"][0].get("term", "")

        articles.append(
            {
                "source": source_name,
                "headline": entry.get("title", ""),
                "sectionName": entry_section,
                "lastModified": last_modified,
                "webUrl": entry.get("link", ""),
            }
        )

    logger.info(f"{source_name}: fetched {len(articles)} articles from RSS.")
    return articles
