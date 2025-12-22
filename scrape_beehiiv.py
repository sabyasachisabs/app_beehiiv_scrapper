#!/usr/bin/env python3
"""
Beehiiv Post Scraper
Downloads posts from a Beehiiv-powered website (e.g., superhuman.ai)
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import time
from datetime import datetime
from pathlib import Path
import re
from urllib.parse import urljoin, urlparse


class BeehiivScraper:
    def __init__(self, base_url, output_dir="posts"):
        """
        Initialize the scraper
        
        Args:
            base_url: Base URL of the Beehiiv website (e.g., "https://www.superhuman.ai")
            output_dir: Directory to save downloaded posts
        """
        self.base_url = base_url.rstrip('/')
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def find_rss_feed(self):
        """Try to find RSS feed URL"""
        rss_urls = [
            f"{self.base_url}/feed",
            f"{self.base_url}/rss",
            f"{self.base_url}/feed.xml",
            f"{self.base_url}/rss.xml",
        ]
        
        for url in rss_urls:
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200 and 'xml' in response.headers.get('content-type', '').lower():
                    return url
            except:
                continue
        return None
    
    def get_posts_from_rss(self, rss_url):
        """Extract posts from RSS feed"""
        try:
            response = self.session.get(rss_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            posts = []
            items = soup.find_all('item')
            
            for item in items:
                title = item.find('title')
                link = item.find('link')
                pub_date = item.find('pubDate')
                description = item.find('description')
                content = item.find('content:encoded') or description
                
                post = {
                    'title': title.text if title else 'Untitled',
                    'url': link.text if link else '',
                    'published_date': pub_date.text if pub_date else '',
                    'description': description.text if description else '',
                    'content': content.text if content else '',
                }
                posts.append(post)
            
            return posts
        except Exception as e:
            print(f"Error parsing RSS feed: {e}")
            return []
    
    def get_posts_from_website(self, max_posts=50):
        """Scrape posts directly from the website"""
        posts = []
        post_links = set()  # Use set to avoid duplicates
        
        # Common Beehiiv URL patterns
        url_patterns = [
            f"{self.base_url}/posts",
            f"{self.base_url}/archive",
            f"{self.base_url}",
        ]
        
        # First, collect all post links from main pages
        for base_pattern in url_patterns:
            try:
                response = self.session.get(base_pattern, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Look for post links - Beehiiv typically uses specific class names
                    selectors = [
                        'a[href*="/p/"]',  # Beehiiv post URLs often have /p/ in them
                        'article a',
                        '.post a',
                        '.article a',
                        '[data-post-id]',
                        'a[href*="post"]',
                    ]
                    
                    for selector in selectors:
                        links = soup.select(selector)
                        for link in links:
                            href = link.get('href', '')
                            if href and '/p/' in href:
                                full_url = urljoin(self.base_url, href)
                                # Normalize URL (remove fragments, query params for comparison)
                                normalized = full_url.split('#')[0].split('?')[0]
                                post_links.add(normalized)
                    
                    # Look for pagination links
                    pagination_links = []
                    pagination_selectors = [
                        'a[href*="/posts"]',
                        'a[href*="/archive"]',
                        '.pagination a',
                        '.page-link',
                        'a[rel="next"]',
                    ]
                    
                    for selector in pagination_selectors:
                        links = soup.select(selector)
                        for link in links:
                            href = link.get('href', '')
                            if href and ('/posts' in href or '/archive' in href or '/page' in href.lower()):
                                full_url = urljoin(self.base_url, href)
                                if full_url not in pagination_links and full_url != base_pattern:
                                    pagination_links.append(full_url)
                    
                    # Try pagination pages (limit to 5 pages to avoid too many requests)
                    for pag_url in pagination_links[:5]:
                        try:
                            time.sleep(0.5)  # Small delay between requests
                            pag_response = self.session.get(pag_url, timeout=10)
                            if pag_response.status_code == 200:
                                pag_soup = BeautifulSoup(pag_response.content, 'html.parser')
                                for selector in selectors:
                                    links = pag_soup.select(selector)
                                    for link in links:
                                        href = link.get('href', '')
                                        if href and '/p/' in href:
                                            full_url = urljoin(self.base_url, href)
                                            normalized = full_url.split('#')[0].split('?')[0]
                                            post_links.add(normalized)
                                if len(post_links) >= max_posts:
                                    break
                        except Exception as e:
                            continue
                    
                    if post_links:
                        break
            except Exception as e:
                print(f"Error scraping {base_pattern}: {e}")
                continue
        
        # Convert set to list and limit
        post_links = list(post_links)[:max_posts]
        
        # Now scrape each post
        if post_links:
            print(f"Found {len(post_links)} unique post links")
            for i, link in enumerate(post_links, 1):
                print(f"[{i}/{len(post_links)}] Scraping: {link}")
                post_data = self.scrape_post_page(link)
                if post_data:
                    posts.append(post_data)
                time.sleep(0.5)  # Be respectful with rate limiting
        
        return posts
    
    def scrape_post_page(self, url):
        """Scrape individual post page"""
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try to find title
            title = None
            title_selectors = ['h1', '.post-title', '.article-title', '[data-title]', 'title']
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element:
                    title = element.get_text(strip=True)
                    if title and len(title) > 10:  # Make sure it's a real title
                        break
            
            # Try to find content
            content = None
            content_selectors = [
                'article',
                '.post-content',
                '.article-content',
                '[data-content]',
                'main',
            ]
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text(separator='\n', strip=True)
                    if content and len(content) > 50:
                        break
            
            # Try to find published date
            pub_date = None
            date_selectors = ['time', '.published-date', '.post-date', '[datetime]']
            for selector in date_selectors:
                element = soup.select_one(selector)
                if element:
                    pub_date = element.get('datetime') or element.get_text(strip=True)
                    if pub_date:
                        break
            
            if title or content:
                return {
                    'title': title or 'Untitled',
                    'url': url,
                    'published_date': pub_date or '',
                    'content': content or '',
                    'description': content[:200] + '...' if content and len(content) > 200 else (content or ''),
                }
        except Exception as e:
            print(f"Error scraping post {url}: {e}")
        
        return None
    
    def save_post(self, post, format='json'):
        """Save a post to file"""
        # Create a safe filename from title
        title_safe = re.sub(r'[^\w\s-]', '', post['title'])[:100]
        title_safe = re.sub(r'[-\s]+', '-', title_safe)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{title_safe}" if title_safe else f"post_{timestamp}"
        
        if format == 'json':
            filepath = self.output_dir / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(post, f, indent=2, ensure_ascii=False)
        elif format == 'txt':
            filepath = self.output_dir / f"{filename}.txt"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {post['title']}\n")
                f.write(f"URL: {post['url']}\n")
                f.write(f"Published: {post.get('published_date', 'N/A')}\n")
                f.write(f"\n{'='*50}\n\n")
                f.write(post.get('content', post.get('description', '')))
        elif format == 'csv':
            # CSV format saves all posts in one file, so this method won't be used for CSV
            # Individual post saving is handled in download_posts method
            pass
        
        return None
    
    def save_posts_to_csv(self, posts):
        """Save all posts to a single CSV file"""
        if not posts:
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_path = self.output_dir / f"posts_{timestamp}.csv"
        
        # Define CSV columns
        fieldnames = ['title', 'url', 'published_date', 'description', 'content']
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            
            for post in posts:
                # Clean content for CSV (remove newlines that might break CSV structure)
                row = {
                    'title': post.get('title', ''),
                    'url': post.get('url', ''),
                    'published_date': post.get('published_date', ''),
                    'description': post.get('description', '').replace('\n', ' ').replace('\r', ''),
                    'content': post.get('content', '').replace('\n', ' ').replace('\r', ''),
                }
                writer.writerow(row)
        
        return csv_path
    
    def download_posts(self, use_rss=True, max_posts=50, format='json'):
        """
        Main method to download posts
        
        Args:
            use_rss: Try to use RSS feed first (faster and more reliable)
            max_posts: Maximum number of posts to download
            format: Output format ('json', 'txt', or 'csv')
        """
        print(f"Starting to download posts from {self.base_url}")
        posts = []
        
        # Try RSS feed first
        if use_rss:
            print("Looking for RSS feed...")
            rss_url = self.find_rss_feed()
            if rss_url:
                print(f"Found RSS feed: {rss_url}")
                posts = self.get_posts_from_rss(rss_url)
                print(f"Found {len(posts)} posts in RSS feed")
            else:
                print("No RSS feed found, scraping website directly...")
        
        # If no RSS or not enough posts, scrape website
        if not posts or len(posts) < max_posts:
            if not use_rss or len(posts) < max_posts:
                print("Scraping website for additional posts...")
                remaining = max_posts - len(posts)
                website_posts = self.get_posts_from_website(max_posts=remaining)
                # Merge posts, avoiding duplicates
                existing_urls = {p['url'] for p in posts}
                for post in website_posts:
                    if post['url'] not in existing_urls:
                        posts.append(post)
                        if len(posts) >= max_posts:
                            break
        
        # Limit to max_posts
        posts = posts[:max_posts]
        
        # Save posts based on format
        print(f"\nSaving {len(posts)} posts...")
        saved_files = []
        
        if format == 'csv':
            # Save all posts to a single CSV file
            print("Saving all posts to CSV file...")
            csv_path = self.save_posts_to_csv(posts)
            if csv_path:
                saved_files.append(csv_path)
                print(f"✓ Saved all posts to: {csv_path}")
        else:
            # Save individual files for JSON and TXT
            for i, post in enumerate(posts, 1):
                print(f"[{i}/{len(posts)}] Saving: {post['title'][:50]}...")
                filepath = self.save_post(post, format=format)
                if filepath:
                    saved_files.append(filepath)
        
        # Create summary
        summary = {
            'website': self.base_url,
            'total_posts': len(posts),
            'downloaded_at': datetime.now().isoformat(),
            'format': format,
            'posts': [{'title': p['title'], 'url': p['url']} for p in posts]
        }
        
        summary_path = self.output_dir / 'summary.json'
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully downloaded {len(posts)} posts")
        print(f"✓ Posts saved to: {self.output_dir}")
        print(f"✓ Summary saved to: {summary_path}")
        
        return posts


def normalize_url(url):
    """Normalize and validate URL"""
    url = url.strip()
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Add https:// if not provided
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    return url


def get_website_url():
    """Prompt user for Beehiiv website URL"""
    while True:
        url = input("\nEnter the Beehiiv newsletter website URL (e.g., https://www.superhuman.ai or superhuman.ai): ").strip()
        
        if not url:
            print("❌ URL cannot be empty. Please try again.")
            continue
        
        try:
            url = normalize_url(url)
            # Basic validation - check if it looks like a URL
            if '.' not in url.replace('https://', '').replace('http://', ''):
                print("❌ Invalid URL format. Please enter a valid website URL.")
                continue
            return url
        except Exception as e:
            print(f"❌ Error processing URL: {e}. Please try again.")
            continue


def get_number_of_posts():
    """Prompt user for number of posts to scrape"""
    while True:
        try:
            num_posts = input("\nEnter the number of posts to scrape (default: 50): ").strip()
            
            if not num_posts:
                return 50  # Default value
            
            num_posts = int(num_posts)
            
            if num_posts <= 0:
                print("❌ Number of posts must be greater than 0. Please try again.")
                continue
            
            if num_posts > 1000:
                confirm = input(f"⚠️  You requested {num_posts} posts. This may take a while. Continue? (y/n): ").strip().lower()
                if confirm != 'y':
                    continue
            
            return num_posts
        except ValueError:
            print("❌ Please enter a valid number.")
            continue


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Download posts from any Beehiiv-powered website',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (will prompt for website and number of posts)
  python scrape_beehiiv.py
  
  # Command-line mode
  python scrape_beehiiv.py --url https://www.superhuman.ai --max-posts 50
  
  # Custom output directory
  python scrape_beehiiv.py --url https://example.beehiiv.com --max-posts 20 --output my_posts
        """
    )
    parser.add_argument('--url', default=None,
                       help='Base URL of the Beehiiv website (if not provided, will prompt)')
    parser.add_argument('--output', default='posts',
                       help='Output directory for downloaded posts (default: posts)')
    parser.add_argument('--max-posts', type=int, default=None,
                       help='Maximum number of posts to download (if not provided, will prompt)')
    parser.add_argument('--format', choices=['json', 'txt', 'csv'], default='csv',
                       help='Output format (default: csv)')
    parser.add_argument('--no-rss', action='store_true',
                       help='Skip RSS feed and scrape website directly')
    
    args = parser.parse_args()
    
    # Show header if running in interactive mode
    if not args.url or args.max_posts is None:
        print("=" * 60)
        print("🐝 Beehiiv Post Scraper")
        print("=" * 60)
    
    # Get website URL (from args or prompt)
    if args.url:
        website_url = normalize_url(args.url)
    else:
        website_url = get_website_url()
    
    # Get number of posts (from args or prompt)
    if args.max_posts is not None:
        max_posts = args.max_posts
    else:
        max_posts = get_number_of_posts()
    
    # Validate inputs
    if max_posts <= 0:
        print("❌ Error: Number of posts must be greater than 0")
        return
    
    print(f"\n📋 Configuration:")
    print(f"   Website: {website_url}")
    print(f"   Posts to scrape: {max_posts}")
    print(f"   Output format: {args.format}")
    print(f"   Output directory: {args.output}")
    print()
    
    scraper = BeehiivScraper(website_url, output_dir=args.output)
    scraper.download_posts(use_rss=not args.no_rss, max_posts=max_posts, format=args.format)


if __name__ == '__main__':
    main()

