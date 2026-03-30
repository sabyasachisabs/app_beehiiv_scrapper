### Each commit will trigger action to update github pages.

# Beehiiv Post Scraper

A generic Python script to download posts from any Beehiiv-powered website. Works with any Beehiiv newsletter or publication.

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

### Interactive Mode (Recommended)

Simply run the script and it will prompt you for the website URL and number of posts:

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # On Windows: venv\Scripts\activate

python scrape_beehiiv.py
```

The script will ask you:
1. **Beehiiv website URL**: Enter the full URL (e.g., `https://www.superhuman.ai`) or just the domain (e.g., `superhuman.ai`)
2. **Number of posts**: Enter how many posts you want to scrape (default: 50)

### Command-Line Mode

You can also provide all options via command-line arguments:

```bash
# Download from a specific website with specific number of posts
python scrape_beehiiv.py --url https://www.superhuman.ai --max-posts 50

# Download from any Beehiiv website
python scrape_beehiiv.py --url https://example.beehiiv.com --max-posts 20

# Save as CSV (default - all posts in one file)
python scrape_beehiiv.py --url https://example.beehiiv.com --format csv

# Save as text files instead
python scrape_beehiiv.py --url https://example.beehiiv.com --format txt

# Save as JSON files
python scrape_beehiiv.py --url https://example.beehiiv.com --format json

# Skip RSS feed and scrape directly
python scrape_beehiiv.py --url https://example.beehiiv.com --no-rss

# Custom output directory
python scrape_beehiiv.py --url https://example.beehiiv.com --output my_posts
```

### Command Line Arguments

- `--url`: Base URL of the Beehiiv website (if not provided, will prompt interactively)
- `--output`: Output directory for downloaded posts (default: posts)
- `--max-posts`: Maximum number of posts to download (if not provided, will prompt interactively)
- `--format`: Output format - 'csv', 'json', or 'txt' (default: csv)
- `--no-rss`: Skip RSS feed and scrape website directly

**Note**: If you don't provide `--url` or `--max-posts`, the script will run in interactive mode and prompt you for these values.

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

## Examples

### Interactive Mode Example

```bash
python scrape_beehiiv.py
```

Output:
```
============================================================
🐝 Beehiiv Post Scraper
============================================================

Enter the Beehiiv newsletter website URL (e.g., https://www.superhuman.ai or superhuman.ai): superhuman.ai

Enter the number of posts to scrape (default: 50): 25

📋 Configuration:
   Website: https://superhuman.ai
   Posts to scrape: 25
   Output format: csv
   Output directory: posts
```

### Command-Line Example

```bash
python scrape_beehiiv.py --url https://www.superhuman.ai --max-posts 10 --format csv
```

This will download the latest 10 posts from superhuman.ai and save them in a single CSV file in the `posts/` directory.

## Notes

- The script respects rate limits with delays between requests
- RSS feeds are preferred as they're faster and more reliable
- If RSS feed is not available, the script will attempt to scrape the website directly
- Make sure you have permission to scrape the target website and comply with their terms of service

