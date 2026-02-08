import os
import html
import base64
import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from email.message import EmailMessage
from typing import List, Dict, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _get_gmail_service():
    """Authenticates and returns a Gmail API service instance."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def _render_article_card(a: Dict[str, Any], cet: ZoneInfo) -> str:
    """Renders a single article as an HTML card."""
    url = a.get("webUrl", "")
    source = html.escape(a.get("source", "Unknown"))
    last_modified_raw = a.get("lastModified", "")
    if last_modified_raw:
        utc_dt = datetime.fromisoformat(last_modified_raw.replace("Z", "+00:00"))
        cet_dt = utc_dt.astimezone(cet)
        last_modified_cet = cet_dt.strftime("%Y %B %-d at %H:%M %Z")
    else:
        last_modified_cet = "N/A"
    headline_safe = html.escape(a.get("headline", ""))
    section_safe = html.escape(a.get("sectionName", ""))
    return (
        f'<div style="margin-bottom: 20px; padding: 12px; border-left: 4px solid #005689; background-color: #f6f6f6;">'
        f'  <h3 style="margin: 0 0 8px 0;"><a href="{url}" style="color: #005689; text-decoration: none;">{headline_safe}</a></h3>'
        f'  <p style="margin: 4px 0; color: #555;"><strong>Source:</strong> {source}</p>'
        f'  <p style="margin: 4px 0; color: #555;"><strong>Section:</strong> {section_safe}</p>'
        f'  <p style="margin: 4px 0; color: #555;"><strong>Last Updated:</strong> {last_modified_cet}</p>'
        f"</div>"
    )


def _get_article_dt(article: Dict[str, Any]) -> datetime:
    """Parses an article's lastModified into a timezone-aware UTC datetime."""
    raw = article.get("lastModified", "")
    if not raw:
        return datetime.min.replace(tzinfo=timezone.utc)
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _bucket_articles(articles: List[Dict[str, Any]], now: datetime) -> List[tuple]:
    """
    Splits articles into time-based sections.
    Returns a list of (heading, articles_list) tuples,
    omitting empty sections.
    """
    buckets = {
        "In the last hour": [],
        "In the last 6 hours": [],
        "In the last 24 hours": [],
    }

    one_hour = timedelta(hours=1)
    six_hours = timedelta(hours=6)
    twenty_four_hours = timedelta(hours=24)

    for a in articles:
        age = now - _get_article_dt(a)
        if age <= one_hour:
            buckets["In the last hour"].append(a)
        elif age <= six_hours:
            buckets["In the last 6 hours"].append(a)
        elif age <= twenty_four_hours:
            buckets["In the last 24 hours"].append(a)
        # Articles older than 24h are still included — in the 24h bucket
        else:
            buckets["In the last 24 hours"].append(a)

    # Sort each bucket newest first
    for articles_list in buckets.values():
        articles_list.sort(key=_get_article_dt, reverse=True)

    # Only return non-empty sections
    return [(heading, items) for heading, items in buckets.items() if items]


def send_email_for_user(
    articles: List[Dict[str, Any]],
    sender: str,
    recipient: str,
    user_name: str = "",
    user_timezone: str = "Europe/Berlin",
) -> None:
    """
    Sends an HTML email to a single user with their pending articles.
    Uses the user's preferred timezone for date formatting.
    Articles are grouped into time-based sections: last hour, last 6 hours, last 24 hours.
    """
    if not articles:
        return

    service = _get_gmail_service()

    subject = f"New Articles for {user_name} ({len(articles)})"
    tz = ZoneInfo(user_timezone)
    now = datetime.now(timezone.utc)

    sections = _bucket_articles(articles, now)

    html_sections = []
    for heading, section_articles in sections:
        cards = "".join(_render_article_card(a, tz) for a in section_articles)
        html_sections.append(
            f'<h2 style="color: #005689; border-bottom: 2px solid #005689; padding-bottom: 6px; margin-top: 30px;">'
            f"{heading} ({len(section_articles)})</h2>"
            f"{cards}"
        )

    greeting = f"Hi {user_name}," if user_name else "Hi,"

    html_body = (
        f'<html><body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">'
        f'<p style="color: #333;">{greeting}</p>'
        f'<h1 style="color: #005689;">Your New Articles ({len(articles)})</h1>'
        f'{"".join(html_sections)}'
        f"</body></html>"
    )

    message = EmailMessage()
    message.set_content(
        "New articles detected. View this email in an HTML-capable client."
    )
    message.add_alternative(html_body, subtype="html")
    message["To"] = recipient
    message["From"] = sender
    message["Subject"] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {"raw": encoded_message}

    logger.info(f"Sending Gmail API email to {recipient}...")
    try:
        send_result = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        logger.info(f"Message Id: {send_result['id']} sent successfully!")
    except Exception as error:
        logger.error(f"Failed to send Gmail API email: {error}")
