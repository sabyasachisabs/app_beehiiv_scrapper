# Beehiiv Post Scraper

A Python script to download posts from Beehiiv-powered websites (e.g., superhuman.ai).

## Features

- Automatically detects and uses RSS feeds when available (faster and more reliable)
- Falls back to web scraping if RSS feed is not found
- Saves posts in CSV, JSON, or TXT format
- Creates a summary file with all downloaded posts
- Respectful rate limiting

## Installation

1. Create a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Download posts from superhuman.ai (default):

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

python scrape_beehiiv.py
```

### Custom Options

```bash
# Download from a different website
python scrape_beehiiv.py --url https://example.beehiiv.com

# Limit number of posts
python scrape_beehiiv.py --max-posts 20

# Save as CSV (default - all posts in one file)
python scrape_beehiiv.py --format csv

# Save as text files instead
python scrape_beehiiv.py --format txt

# Save as JSON files
python scrape_beehiiv.py --format json

# Skip RSS feed and scrape directly
python scrape_beehiiv.py --no-rss

# Custom output directory
python scrape_beehiiv.py --output my_posts
```

### Command Line Arguments

- `--url`: Base URL of the Beehiiv website (default: https://www.superhuman.ai)
- `--output`: Output directory for downloaded posts (default: posts)
- `--max-posts`: Maximum number of posts to download (default: 50)
- `--format`: Output format - 'csv', 'json', or 'txt' (default: csv)
- `--no-rss`: Skip RSS feed and scrape website directly

## Output

The script creates:

1. **Post files**: Posts saved based on format (CSV: single file, JSON/TXT: individual files)
2. **summary.json**: A summary file containing metadata about all downloaded posts

### CSV Format (Default)

All posts are saved in a single CSV file with the following columns:
- `title`: Post title
- `url`: Post URL
- `published_date`: Publication date (if available)
- `description`: Post description/excerpt
- `content`: Full post content

The CSV file is named `posts_YYYYMMDD_HHMMSS.csv` and can be easily opened in Excel, Google Sheets, or any spreadsheet application.

### JSON Format

Each post is saved as a separate JSON file containing:
- `title`: Post title
- `url`: Post URL
- `published_date`: Publication date (if available)
- `content`: Full post content
- `description`: Post description/excerpt

### TXT Format

Each post is saved as a separate TXT file containing:
- Title
- URL
- Published date
- Full content

## Example

```bash
python scrape_beehiiv.py --url https://www.superhuman.ai --max-posts 10 --format csv
```

This will download the latest 10 posts from superhuman.ai and save them in a single CSV file in the `posts/` directory.

## Notes

- The script respects rate limits with delays between requests
- RSS feeds are preferred as they're faster and more reliable
- If RSS feed is not available, the script will attempt to scrape the website directly
- Make sure you have permission to scrape the target website and comply with their terms of service

