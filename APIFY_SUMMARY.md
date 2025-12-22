# Apify Actor - Summary

Your Beehiiv Post Scraper has been successfully converted into an Apify Actor! 🎉

## What Was Created

### Core Files
- **`src/main.py`**: Main Apify actor script that uses the Apify SDK
- **`scrape_beehiiv.py`**: Core scraper class (unchanged, works for both local and Apify)
- **`Dockerfile`**: Docker configuration for containerizing the actor
- **`requirements.txt`**: Updated with Apify SDK dependency

### Apify Configuration
- **`.actor/actor.json`**: Actor metadata and configuration
- **`.actor/input_schema.json`**: Input schema definition for the Apify UI
- **`.actor/README.md`**: Actor documentation for Apify Store
- **`apify.json`**: Apify build configuration

### Documentation
- **`APIFY_DEPLOYMENT.md`**: Complete deployment guide
- **`README.md`**: Original project documentation (still works for local use)

## Quick Start

### 1. Install Apify CLI
```bash
npm install -g apify-cli
```

### 2. Login to Apify
```bash
apify login
```

### 3. Deploy
```bash
apify push
```

### 4. Test
Go to [Apify Console](https://console.apify.com) and run your actor with:
```json
{
  "websiteUrl": "https://www.superhuman.ai",
  "maxPosts": 50,
  "outputFormat": "csv"
}
```

## Key Features

✅ **Apify SDK Integration**: Uses `apify` package for Actor.get_input() and Actor.push_data()  
✅ **Input Schema**: Defined in `.actor/input_schema.json` for user-friendly UI  
✅ **Dataset Output**: Posts are saved to Apify dataset automatically  
✅ **Dockerized**: Ready for Apify's containerized environment  
✅ **Generic**: Works with any Beehiiv website  

## Project Structure

```
app_beehiiv_scrapper/
├── .actor/                    # Apify actor configuration
│   ├── actor.json            # Actor metadata
│   ├── input_schema.json     # Input schema
│   └── README.md             # Actor docs
├── src/
│   └── main.py               # Apify actor entry point
├── scrape_beehiiv.py         # Core scraper (shared)
├── Dockerfile                 # Docker config
├── requirements.txt          # Dependencies (includes apify)
├── apify.json                 # Apify build config
└── APIFY_DEPLOYMENT.md        # Deployment guide
```

## Next Steps

1. **Test Locally** (optional):
   ```bash
   python scrape_beehiiv.py  # Test original script
   ```

2. **Deploy to Apify**:
   ```bash
   apify push
   ```

3. **Publish to Store**:
   - Go to Apify Console
   - Open your actor
   - Click "Publish to Store"
   - Fill in details and submit

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `websiteUrl` | string | ✅ Yes | - | Beehiiv website URL |
| `maxPosts` | integer | ❌ No | 50 | Max posts to scrape |
| `outputFormat` | string | ❌ No | "csv" | "csv", "json", or "txt" |
| `useRss` | boolean | ❌ No | true | Use RSS feed if available |

## Output

Posts are automatically saved to the Apify dataset with this structure:
- `title`: Post title
- `url`: Post URL
- `publishedDate`: Publication date
- `description`: Post description
- `content`: Full post content
- `scrapedAt`: Timestamp when scraped

## Support

- **Apify Docs**: https://docs.apify.com
- **Deployment Guide**: See `APIFY_DEPLOYMENT.md`
- **Local Usage**: See `README.md`

Happy scraping! 🚀

