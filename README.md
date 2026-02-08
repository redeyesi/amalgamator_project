# Amalgamator

A Python application that aggregates news articles from multiple sources (APIs and RSS feeds), deduplicates them using SHA-256 hashes, stores them in a CSV, and sends HTML email notifications via the Gmail API.

## Features

- **Multi-source aggregation** — Guardian API + configurable RSS feeds (BBC, Al Jazeera, NPR, AP, etc.)
- **Deduplication** — SHA-256 hashing of headline + timestamp prevents duplicate articles
- **HTML email notifications** — Time-bucketed sections (last hour / 6 hours / 24 hours) with styled article cards
- **CSV storage** — Persistent article log with date, source, section, headline, URL, and hash
- **Modular architecture** — Easy to add new sources by creating a fetch function that returns the standard article format

## Project Structure

```
amalgamator_project/
    main.py                  # Orchestrator — wires sources, dedup, storage, email
    sources/
        guardian.py          # Guardian Content API source
        rss.py               # Generic RSS/Atom feed source
    utils/
        dedup.py             # Source-agnostic deduplication
        storage.py           # CSV load/save operations
        email_service.py     # Gmail API email with HTML formatting
    testing/                 # Development test scripts
    logs/                    # Timestamped log files (gitignored)
```

## Setup

### Prerequisites

- Python 3.11+
- A Guardian API key — [register here](https://open-platform.theguardian.com/access/)
- Gmail API credentials — [Google Cloud Console](https://console.cloud.google.com/)

### Installation

```bash
# Clone the repo
git clone https://github.com/redeyesi/amalgamator_project.git
cd amalgamator_project

# Create and activate virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file in the project root:

```
GUARDIAN_API_KEY=your_guardian_api_key_here
```

2. Set up Gmail API credentials:
   - Go to [Google Cloud Console](https://console.cloud.google.com/) > APIs & Services > Credentials
   - Create an OAuth 2.0 Client ID (Desktop app)
   - Download the JSON and save as `credentials.json` in the project root
   - On first run, a browser window will open for OAuth consent. This creates `token.json` automatically.

3. Update sender/recipient email addresses in `main.py`:

```python
EMAIL_SENDER = "your-sender@gmail.com"
EMAIL_RECIPIENTS = ["recipient@example.com"]
```

## Usage

```bash
source venv/bin/activate
python main.py
```

The script will:

1. Fetch articles from the Guardian API and all configured RSS feeds
2. Deduplicate against previously seen articles in `articles.csv`
3. Append new articles to the CSV
4. Send an HTML email with new articles grouped by recency

## Adding a New RSS Feed

Add an entry to the `rss_feeds` list in `main.py`:

```python
{
    "feed_url": "https://example.com/rss.xml",
    "source_name": "Example News",
    "section": "World",
},
```

## Standard Article Format

All sources normalise articles to this dict structure:

| Key            | Description                     |
| -------------- | ------------------------------- |
| `source`       | Provider name (e.g. "BBC News") |
| `headline`     | Article title                   |
| `sectionName`  | Section/category label          |
| `lastModified` | ISO 8601 UTC timestamp          |
| `webUrl`       | Link to the full article        |
