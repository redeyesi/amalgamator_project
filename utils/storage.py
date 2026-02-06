import os
import logging
from typing import List, Dict, Any, Set

import pandas as pd

logger = logging.getLogger(__name__)

CSV_COLUMNS = [
    "date_added",
    "lastModified",
    "source",
    "sectionName",
    "headline",
    "webUrl",
    "hash",
]


def load_existing_hashes(file_path: str) -> Set[str]:
    """
    Loads existing article hashes from the CSV to prevent duplicates.
    """
    if not os.path.exists(file_path):
        logger.info(f"{file_path} not found. Starting fresh.")
        return set()

    try:
        df = pd.read_csv(file_path, usecols=["hash"])
        hashes = set(df["hash"].astype(str))
        logger.info(f"Loaded {len(hashes)} existing article hashes.")
        return hashes
    except Exception as e:
        logger.error(f"Error reading existing CSV: {e}")
        return set()


def save_articles(new_rows: List[Dict[str, Any]], file_path: str) -> None:
    """
    Appends new articles to the CSV file.
    """
    if not new_rows:
        logger.info("No new rows to save.")
        return

    df_new = pd.DataFrame(new_rows)

    # Only include columns that exist in the data, in the preferred order
    columns = [c for c in CSV_COLUMNS if c in df_new.columns]
    df_new = df_new[columns]

    file_exists = os.path.exists(file_path)
    write_header = not file_exists

    try:
        df_new.to_csv(file_path, mode="a", header=write_header, index=False)
        logger.info(f"Successfully appended {len(new_rows)} articles to {file_path}.")
    except Exception as e:
        logger.error(f"Failed to save to CSV: {e}")
