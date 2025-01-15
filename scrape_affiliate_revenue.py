from playwright.sync_api import sync_playwright
import json

def scrape_affiliate_revenue():
    """
    Scrapes affiliate revenue data using Playwright.
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

            # Extract additional product information
            product_elements = page.query_selector_all('.product-card')  # Replace with the actual selector for product containers
            for product_element in product_elements:
                try:
                    name = product_element.query_selector('.name')  # Replace with the actual selector for product name
                    text_medium = product_element.query_selector('.text-medium')  # Replace with the actual selector for text-medium
                    price_element = product_element.query_selector('number-flow-react')
                    time_range = product_element.query_selector('.time-range')  # Replace with the actual selector for time range
                    whop_rank = product_element.query_selector('.rank')  # Replace with the actual selector for Whop rank
                    logo = product_element.query_selector('img')  # Replace with the actual selector for logo

                    if name and price_element and time_range and whop_rank and logo:
                        price_data = json.loads(price_element.get_attribute('data'))
                        products.append({
                            "name": name.inner_text(),
                            "text_medium": text_medium.inner_text() if text_medium else None,
                            "price": float(price_data['valueAsString'].replace('$', '').replace(',', '')),
                            "time_range": time_range.inner_text(),
                            "whop_rank": int(whop_rank.inner_text().strip()),
                            "logo": logo.get_attribute('src')
                        })
                except Exception as e:
                    print(f"Error parsing product element: {e}")
                    continue

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