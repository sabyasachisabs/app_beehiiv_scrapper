# Beehiiv Post Scraper - Apify Actor

A powerful Apify Actor that scrapes and downloads posts from any Beehiiv-powered newsletter website.

## Features

- 🚀 **Generic**: Works with any Beehiiv-powered website
- 📡 **RSS Support**: Automatically detects and uses RSS feeds when available
- 🌐 **Web Scraping**: Falls back to direct web scraping if RSS feed is not found
- 📊 **Multiple Formats**: Output posts in CSV, JSON, or TXT format
- ⚡ **Efficient**: Respects rate limits and handles pagination
- 📦 **Apify Integration**: Seamlessly integrates with Apify platform and datasets

## Input

The Actor accepts the following input parameters:

- **websiteUrl** (required): The URL of the Beehiiv-powered website (e.g., `https://www.superhuman.ai` or `superhuman.ai`)
- **maxPosts** (optional, default: 50): Maximum number of posts to scrape
- **outputFormat** (optional, default: "csv"): Output format - "csv", "json", or "txt"
- **useRss** (optional, default: true): Try to use RSS feed first (faster and more reliable)

## Output

The Actor outputs scraped posts to the Apify dataset with the following structure:

```json
{
  "title": "Post Title",
  "url": "https://example.com/p/post-slug",
  "publishedDate": "2025-12-22",
  "description": "Post description/excerpt",
  "content": "Full post content",
  "scrapedAt": "2025-12-22T10:30:00"
}
```

## Usage

### Via Apify Console

1. Go to your Apify account
2. Create a new Actor or use this one
3. Configure the input:
   - Set `websiteUrl` to your target Beehiiv website
   - Adjust `maxPosts` as needed
   - Choose your preferred `outputFormat`
4. Run the Actor
5. Download results from the dataset

### Via Apify API

```bash
curl -X POST "https://api.apify.com/v2/acts/YOUR_ACTOR_ID/run" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "websiteUrl": "https://www.superhuman.ai",
    "maxPosts": 50,
    "outputFormat": "csv",
    "useRss": true
  }'
```

## Examples

### Scrape 50 posts from superhuman.ai

```json
{
  "websiteUrl": "https://www.superhuman.ai",
  "maxPosts": 50,
  "outputFormat": "csv"
}
```

### Scrape 100 posts from another Beehiiv site

```json
{
  "websiteUrl": "https://example.beehiiv.com",
  "maxPosts": 100,
  "outputFormat": "json",
  "useRss": false
}
```

## Development

### Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Test locally:
```bash
apify run
```

### Deployment

1. Login to Apify:
```bash
apify login
```

2. Push to Apify:
```bash
apify push
```

## Notes

- The Actor respects rate limits with delays between requests
- RSS feeds are preferred as they're faster and more reliable
- If RSS feed is not available, the Actor will attempt to scrape the website directly
- Make sure you have permission to scrape the target website and comply with their terms of service

## Support

For issues or questions, please open an issue on the GitHub repository.

