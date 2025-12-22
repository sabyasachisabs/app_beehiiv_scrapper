# Apify Actor Deployment Guide

This guide will help you deploy the Beehiiv Post Scraper as an Apify Actor to the Apify Store.

## Prerequisites

1. **Node.js**: Install Node.js from [nodejs.org](https://nodejs.org/)
2. **Apify Account**: Create an account at [apify.com](https://apify.com)
3. **Apify CLI**: Install the Apify CLI globally:
   ```bash
   npm install -g apify-cli
   ```

## Project Structure

```
app_beehiiv_scrapper/
├── .actor/
│   ├── actor.json          # Actor metadata
│   ├── input_schema.json   # Input schema definition
│   └── README.md          # Actor documentation
├── src/
│   └── main.py            # Main actor script
├── scrape_beehiiv.py      # Scraper class
├── Dockerfile              # Docker configuration
├── requirements.txt       # Python dependencies
├── apify.json             # Apify configuration
└── README.md              # Project documentation
```

## Local Development

### 1. Install Dependencies

```bash
# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Test Locally

You can test the scraper locally before deploying:

```bash
# Test the original script
python scrape_beehiiv.py

# Or test with Apify CLI (if you have Apify SDK set up)
apify run
```

## Deployment to Apify

### 1. Login to Apify

```bash
apify login
```

Enter your Apify API token when prompted. You can find your API token in your [Apify account settings](https://console.apify.com/account/integrations).

### 2. Initialize Actor (if needed)

If you haven't already, initialize the actor:

```bash
apify init
```

This will create the `.actor` directory structure if it doesn't exist.

### 3. Build and Push

```bash
# Build the actor
apify build

# Push to Apify platform
apify push
```

The `apify push` command will:
- Build a Docker image
- Upload it to Apify
- Create/update the actor in your Apify account

### 4. Test on Apify Platform

1. Go to [Apify Console](https://console.apify.com)
2. Find your actor in "My Actors"
3. Click on it to open the actor page
4. Configure input and click "Start" to test

## Publishing to Apify Store

Once your actor is working correctly:

1. **Go to Actor Settings**: In your actor page, click on "Settings"
2. **Fill in Store Information**:
   - Title: "Beehiiv Post Scraper"
   - Description: Add a detailed description
   - Categories: Select relevant categories (e.g., "Web Scraping", "Content")
   - Tags: Add relevant tags
   - Pricing: Set your pricing model (Free, Pay-per-use, etc.)
3. **Add Screenshots/Demo**: Upload screenshots or create a demo video
4. **Submit for Review**: Click "Publish to Store"
5. **Wait for Approval**: Apify team will review your actor

## Input Schema

The actor accepts the following input (defined in `.actor/input_schema.json`):

```json
{
  "websiteUrl": "https://www.superhuman.ai",  // Required
  "maxPosts": 50,                              // Optional, default: 50
  "outputFormat": "csv",                       // Optional: "csv", "json", "txt"
  "useRss": true                               // Optional, default: true
}
```

## Output

The actor outputs data to the Apify dataset with the following structure:

```json
{
  "title": "Post Title",
  "url": "https://example.com/p/post-slug",
  "publishedDate": "2025-12-22",
  "description": "Post description",
  "content": "Full post content",
  "scrapedAt": "2025-12-22T10:30:00"
}
```

## Troubleshooting

### Build Errors

If you encounter build errors:

1. Check Dockerfile syntax
2. Verify all dependencies in requirements.txt
3. Ensure Python version compatibility

### Runtime Errors

If the actor fails at runtime:

1. Check Apify logs in the console
2. Verify input schema matches expected format
3. Test locally first to identify issues

### Import Errors

If you see import errors:

1. Verify all dependencies are in requirements.txt
2. Check file paths in Dockerfile
3. Ensure scrape_beehiiv.py is copied correctly

## Updating the Actor

To update your actor after making changes:

```bash
# Make your changes to the code
# Then push again
apify push
```

The new version will be available in your Apify account.

## Best Practices

1. **Version Control**: Use git to track changes
2. **Testing**: Always test locally before pushing
3. **Documentation**: Keep README and input schema up to date
4. **Error Handling**: Add proper error handling and logging
5. **Rate Limiting**: Respect website rate limits
6. **Legal Compliance**: Ensure you have permission to scrape target websites

## Support

- Apify Documentation: https://docs.apify.com
- Apify Community: https://forum.apify.com
- GitHub Issues: Open an issue in the repository

## License

Make sure to specify a license in your actor.json file if you plan to publish it.

