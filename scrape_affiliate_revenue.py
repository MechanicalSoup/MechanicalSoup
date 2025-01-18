from playwright.sync_api import sync_playwright
import json
from firecrawl import FirecrawlApp
from pydantic import BaseModel

class ProductSchema(BaseModel):
    name: str
    description: str
    price: str
    ranking: str
    time_range: str
    logo: str

def scrape_affiliate_revenue():
    """
    Scrapes affiliate revenue data using Playwright and Firecrawl.dev API.
    Returns revenue data as a dictionary.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            # Navigate to the URL
            page.goto("https://whop.com/discover/f/most_affiliate_earnings_24_hours/")

            # Wait for and extract number-flow-react elements
            elements = page.query_selector_all('number-flow-react')
            platform_metrics = {
                "total_revenue": None,
                "total_users": None
            }
            affiliate_earnings = []
            products = []

            for element in elements:
                try:
                    # Get data attribute from shadow DOM element
                    data_attr = element.get_attribute('data')
                    if data_attr:
                        data = json.loads(data_attr)
                        value = data.get('valueAsString') or data.get('value')
                        print(f"Found value: {value}")  # Debug print
                        
                        # Classify the values
                        if value and isinstance(value, str):
                            value = value.replace('$', '')
                            if float(value.replace(',', '')) > 500000:  # Likely platform metric
                                if ',' in value and len(value) > 10:  # Total revenue
                                    platform_metrics["total_revenue"] = value
                                else:  # User count
                                    platform_metrics["total_users"] = value
                            else:  # Regular affiliate earning
                                affiliate_earnings.append(value)
                except Exception as e:
                    print(f"Error parsing element: {e}")
                    continue

            # Use Firecrawl.dev API to extract product information
            api_key = "fc-26d2bf277d8647a3a1c01203a536d757"
            app = FirecrawlApp(api_key=api_key)
            response = app.scrape_url(
                'https://whop.com/discover/f/most_affiliate_earnings_24_hours/',
                params={
                    'formats': ['extract'],
                    'extract': {
                        'schema': ProductSchema.model_json_schema(),
                    }
                }
            )

            if response['success']:
                data = response['data']
                products = data.get("extract", [])
                with open('scraped_data.json', 'w') as f:
                    json.dump(data, f, indent=2)
            else:
                print(f"Error fetching data: {response}")

            print(f"\nFound metrics: {platform_metrics}")  # Debug print
            print(f"Found earnings: {affiliate_earnings}")  # Debug print
            print(f"Found products: {products}")  # Debug print
            
            return {
                "platform_metrics": platform_metrics,
                "affiliate_earnings": affiliate_earnings,
                "products": products
            }

        except Exception as e:
            print(f"Error during scraping: {e}")
            return {}
        finally:
            browser.close()

if __name__ == "__main__":
    result = scrape_affiliate_revenue()  # Store the result
    print("\nRaw scraped data:")
    print(json.dumps(result, indent=2))  # Print formatted output