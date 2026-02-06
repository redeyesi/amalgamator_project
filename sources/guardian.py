import logging
from typing import List, Dict, Any

import requests

logger = logging.getLogger(__name__)

API_URL = "https://content.guardianapis.com/search"

DEFAULT_PARAMS = {
    "format": "json",
    "order-by": "newest",
    "query-fields": "headline,body",
    "show-fields": "headline,byline,publication,lastModified,wordcount",
    "shouldHideAdverts": "true",
    "page-size": 5,
    "section": "world",
}


def fetch(api_key: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Fetches articles from the Guardian API and returns them in a
    standardised format.
    """
    if not api_key:
        logger.error("Guardian API Key is missing.")
        raise ValueError("GUARDIAN_API_KEY not found in environment variables.")

    request_params = (params or DEFAULT_PARAMS).copy()
    request_params["api-key"] = api_key

    logger.debug(f"Requesting Guardian API with params: {params or DEFAULT_PARAMS}")

    try:
        response = requests.get(API_URL, params=request_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        raw_articles = data.get("response", {}).get("results", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Guardian API request failed: {e}")
        return []

    # Normalise to standard article format
    articles = []
    for article in raw_articles:
        fields = article.get("fields", {})
        articles.append(
            {
                "source": "The Guardian",
                "headline": fields.get("headline", ""),
                "sectionName": article.get("sectionName", ""),
                "lastModified": fields.get("lastModified", ""),
                "webUrl": article.get("webUrl", ""),
            }
        )

    logger.info(f"Guardian: fetched {len(articles)} articles.")
    return articles
