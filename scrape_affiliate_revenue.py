# This file contains the scraping logic but is not directly executed
# All functionality is accessed through process_revenue_data.py which generates combined_data.json

# ...existing code commented out...

from playwright.sync_api import sync_playwright
from firecrawl import FirecrawlApp
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def scrape_metrics_with_playwright():
    """Scrape revenue metrics and affiliate earnings from all pages"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        platform_metrics = {"total_revenue": None, "total_users": None}
        all_affiliate_earnings = []
        
        try:
            # Get platform metrics from first page only
            page.goto("https://whop.com/discover/f/most_affiliate_earnings_24_hours/")
            elements = page.query_selector_all('number-flow-react')
            
            # Process first page metrics
            for element in elements:
                try:
                    data_attr = element.get_attribute('data')
                    if data_attr:
                        data = json.loads(data_attr)
                        value = data.get('valueAsString') or data.get('value')
                        
                        if value and isinstance(value, str):
                            value = value.replace('$', '')
                            if float(value.replace(',', '')) > 500000:
                                if ',' in value and len(value) > 10:
                                    platform_metrics["total_revenue"] = value
                                else:
                                    platform_metrics["total_users"] = value
                            else:
                                all_affiliate_earnings.append(value)
                except Exception as e:
                    print(f"Error parsing element: {e}")

            # Scrape additional pages
            for page_num in range(2, 6):  # Pages 2-5
                url = f"https://whop.com/discover/f/most_affiliate_earnings_24_hours/p/{page_num}/"
                print(f"Scraping page {page_num}: {url}")
                
                page.goto(url)
                elements = page.query_selector_all('number-flow-react')
                
                # Process affiliate earnings from additional pages
                for element in elements:
                    try:
                        data_attr = element.get_attribute('data')
                        if data_attr:
                            data = json.loads(data_attr)
                            value = data.get('valueAsString') or data.get('value')
                            if value and isinstance(value, str):
                                value = value.replace('$', '')
                                if float(value.replace(',', '')) < 500000:  # Only affiliate earnings
                                    all_affiliate_earnings.append(value)
                    except Exception as e:
                        print(f"Error parsing element on page {page_num}: {e}")
            
            return platform_metrics, all_affiliate_earnings
                    
        finally:
            browser.close()

def scrape_products_with_firecrawl():
    """Scrape products from all pages using Firecrawl"""
    try:
        app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))
        all_communities = []

        # Scrape each page
        for page_num in range(1, 6):  # Pages 1-5
            url = f"https://whop.com/discover/f/most_affiliate_earnings_24_hours/"
            if page_num > 1:
                url += f"p/{page_num}/"
                
            print(f"Scraping communities from page {page_num}: {url}")
            
            params = {
                'formats': ['extract'],
                'extract': {
                    'schema': {
                        "type": "object",
                        "properties": {
                            "top_communities": {
                                "type": "array",
                                "selector": "div[class*='product-card']",  # Updated selector
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {
                                            "type": "string",
                                            "selector": "div[class*='fui-Text']"  # Updated selector
                                        },
                                        "price_per_unit": {
                                            "type": "string",
                                            "selector": "number-flow-react",
                                            "attribute": "data"
                                        },
                                        "logo": {
                                            "type": "string",
                                            "selector": "img",
                                            "attribute": "src"
                                        },
                                        "title": {
                                            "type": "string",
                                            "selector": "div[class*='whitespace-pre-wrap']"  # Updated selector
                                        },
                                        "other_information": {
                                            "type": "string",
                                            "selector": "span[class*='text-medium']"  # Updated selector
                                        },
                                        "whop_rank": {
                                            "type": "string",
                                            "selector": "span[class*='flex items-center gap-1']"  # Updated selector
                                        }
                                    }
                                }
                            }
                        },
                        "required": ["top_communities"]
                    }
                }
            }
            
            response = app.scrape_url(url, params=params)
            
            # Extract communities from this page
            communities = response.get('extract', {}).get('top_communities', [])
            if not communities:
                communities = response.get('data', {}).get('extract', {}).get('top_communities', [])
            
            if communities:
                all_communities.extend(communities)
            
            print(f"Found {len(communities)} communities on page {page_num}")
            
        return all_communities
        
    except Exception as e:
        print(f"Error during Firecrawl scraping: {e}")
        return []

def scrape_affiliate_revenue():
    """Main scraping function combining both methods"""
    try:
        platform_metrics, affiliate_earnings = scrape_metrics_with_playwright()
        
        # Get and validate communities data
        communities = scrape_products_with_firecrawl()
        if not communities and os.path.exists('debug_scraped_data.json'):
            # Try to recover communities from debug file if scraping failed
            with open('debug_scraped_data.json', 'r') as f:
                debug_data = json.load(f)
                communities = debug_data.get('extract', {}).get('top_communities', [])
        
        result = {
            "platform_metrics": platform_metrics,
            "affiliate_earnings": affiliate_earnings,
            "top_communities": communities
        }
        
        # Save raw data with absolute path
        output_path = os.path.join(os.path.dirname(__file__), 'data', 'scraped_data.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
            print(f"Data saved to {output_path}")
            
        return result

    except Exception as e:
        print(f"Error in scrape_affiliate_revenue: {e}")
        return None

if __name__ == "__main__":
    result = scrape_affiliate_revenue()
    print("\nRaw scraped data:")
    print(json.dumps(result, indent=2))