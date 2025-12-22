#!/usr/bin/env python3
"""
Apify Actor - Beehiiv Post Scraper
Downloads posts from any Beehiiv-powered website
"""

from apify import Actor
import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path to import scrape_beehiiv
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from scrape_beehiiv import BeehiivScraper, normalize_url


async def main():
    async with Actor:
        # Get input from Apify
        actor_input = await Actor.get_input() or {}
        
        website_url = actor_input.get('websiteUrl')
        max_posts = actor_input.get('maxPosts', 50)
        output_format = actor_input.get('outputFormat', 'csv')
        use_rss = actor_input.get('useRss', True)
        
        # Validate required input
        if not website_url:
            await Actor.fail('Missing required input: websiteUrl')
            return
        
        # Normalize URL
        website_url = normalize_url(website_url)
        
        await Actor.log.info(f'Starting to scrape posts from: {website_url}')
        await Actor.log.info(f'Configuration: maxPosts={max_posts}, format={output_format}, useRss={use_rss}')
        
        # Initialize scraper
        scraper = BeehiivScraper(website_url, output_dir='./storage')
        
        # Download posts
        posts = scraper.download_posts(
            use_rss=use_rss,
            max_posts=max_posts,
            format=output_format
        )
        
        # Add scraped timestamp to each post
        scraped_at = datetime.now().isoformat()
        
        # Save posts to Apify dataset
        await Actor.log.info(f'Saving {len(posts)} posts to Apify dataset...')
        
        for post in posts:
            # Prepare data for Apify dataset
            dataset_item = {
                'title': post.get('title', ''),
                'url': post.get('url', ''),
                'publishedDate': post.get('published_date', ''),
                'description': post.get('description', ''),
                'content': post.get('content', ''),
                'scrapedAt': scraped_at,
            }
            
            # Push to dataset
            await Actor.push_data(dataset_item)
        
        await Actor.log.info(f'✓ Successfully scraped and saved {len(posts)} posts')
        
        # Set output statistics
        output_stats = {
            'totalPosts': len(posts),
            'website': website_url,
            'format': output_format,
            'posts': [{'title': p['title'], 'url': p['url']} for p in posts]
        }
        
        await Actor.set_value('OUTPUT', output_stats)


if __name__ == '__main__':
    asyncio.run(main())

