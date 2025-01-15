from scrape_affiliate_revenue import scrape_affiliate_revenue
from typing import List, Dict
import re

def clean_monetary_value(value: str) -> float:
    """Convert string monetary values to float"""
    if isinstance(value, (int, float)):
        return float(value)
    return float(re.sub(r'[^\d.]', '', value))

def process_revenue_data() -> Dict:
    """Process scraped revenue data"""
    raw_data = scrape_affiliate_revenue()
    
    clean_data = {
        "platform_metrics": {
            "total_revenue": None,
            "total_users": None
        },
        "affiliate_earnings": set()
    }

    # Handle platform metrics
    if raw_data.get("platform_metrics"):
        metrics = raw_data["platform_metrics"]
        if metrics["total_revenue"]:
            clean_data["platform_metrics"]["total_revenue"] = clean_monetary_value(metrics["total_revenue"])
        if metrics["total_users"]:
            clean_data["platform_metrics"]["total_users"] = int(re.sub(r'[^\d]', '', metrics["total_users"]))

    # Handle affiliate earnings
    for value in raw_data.get("affiliate_earnings", []):
        try:
            cleaned_value = clean_monetary_value(value)
            if cleaned_value > 0 and cleaned_value < 500000:  # Sanity check
                clean_data["affiliate_earnings"].add(cleaned_value)
        except ValueError:
            continue

    return {
        "platform_metrics": clean_data["platform_metrics"],
        "affiliate_earnings": sorted(list(clean_data["affiliate_earnings"]), reverse=True)
    }

if __name__ == "__main__":
    results = process_revenue_data()
    
    # Check if we have valid data
    if results["platform_metrics"]["total_revenue"] is not None:
        print("\nPlatform Metrics:")
        print(f"Total Revenue: ${results['platform_metrics']['total_revenue']:,.2f}")
        print(f"Total Users: {results['platform_metrics']['total_users']:,}")
    else:
        print("No platform metrics found!")

    if results["affiliate_earnings"]:
        print("\nAffiliate Earnings:")
        for earning in results["affiliate_earnings"]:
            print(f"${earning:,.2f}")
    else:
        print("No affiliate earnings found!")

    # Debug info
    print("\nRaw results:")
    print(results)
