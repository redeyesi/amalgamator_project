import hashlib
import logging
from datetime import datetime
from typing import List, Dict, Any, Set

logger = logging.getLogger(__name__)


def deduplicate(
    articles: List[Dict[str, Any]], seen_hashes: Set[str]
) -> List[Dict[str, Any]]:
    """
    Generates hashes for articles and filters out duplicates.
    Expects articles in the standardised format (with 'headline' and 'lastModified').
    Returns a list of new article dicts with 'date_added' and 'hash' fields added.
    """
    new_rows = []

    for article in articles:
        headline = article.get("headline", "")
        last_modified = article.get("lastModified", "")

        hash_input = headline + last_modified
        article_hash = hashlib.sha256(hash_input.encode()).hexdigest()

        logger.debug(f"Processing: '{headline}' | Hash: {article_hash}")

        if article_hash not in seen_hashes:
            logger.info(f"New article detected: {headline}")
            row = article.copy()
            row["date_added"] = datetime.now().isoformat()
            row["hash"] = article_hash
            new_rows.append(row)
            seen_hashes.add(article_hash)
        else:
            logger.debug(f"Duplicate skipped: {headline}")

    return new_rows
