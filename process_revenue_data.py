from scrape_affiliate_revenue import scrape_affiliate_revenue
from typing import List, Dict
import re
import os
import json

def clean_monetary_value(value: str) -> float:
    """Convert string monetary values to float"""
    if isinstance(value, (int, float)):
        return float(value)
    return float(re.sub(r'[^\d.]', '', value))

def process_revenue_data() -> Dict:
    """Process scraped revenue data and combine affiliate earnings with communities"""
    raw_data = scrape_affiliate_revenue()
    
    if raw_data is None:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'scraped_data.json')
        try:
            with open(data_path, 'r') as f:
                raw_data = json.load(f)
        except Exception as e:
            print(f"Error loading saved data: {e}")
            return {}

    # Clean and process platform metrics
    clean_data = {
        "platform_metrics": {
            "total_revenue": None,
            "total_users": None
        },
        "top_communities": []  # Changed back to top_communities to match desired format
    }

    # Process platform metrics
    if raw_data.get("platform_metrics"):
        metrics = raw_data["platform_metrics"]
        if metrics["total_revenue"]:
            clean_data["platform_metrics"]["total_revenue"] = clean_monetary_value(metrics["total_revenue"])
        if metrics["total_users"]:
            clean_data["platform_metrics"]["total_users"] = int(re.sub(r'[^\d]', '', metrics["total_users"]))

    # Get raw data lists
    earnings = raw_data.get("affiliate_earnings", [])
    communities = raw_data.get("top_communities", [])
    
    # Merge data while keeping original string format of earnings
    for idx, community in enumerate(communities):
        if idx < len(earnings):
            community_copy = dict(community)
            # Add affiliate_earnings in the original string format
            community_copy["affiliate_earnings"] = earnings[idx]
            clean_data["top_communities"].append(community_copy)
    
    # Save processed data
    output_path = os.path.join(os.path.dirname(__file__), 'data', 'processed_data.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(clean_data, f, indent=2)
        print(f"Processed data saved to {output_path}")

    return clean_data

if __name__ == "__main__":
    results = process_revenue_data()
    
    if results["platform_metrics"]["total_revenue"] is not None:
        print("\nPlatform Summary:")
        print(f"Total Revenue: ${results['platform_metrics']['total_revenue']:,.2f}")
        print(f"Total Users: {results['platform_metrics']['total_users']:,}")
        print(f"\nTop Communities: {len(results['top_communities'])}")
        
        for community in results['top_communities']:
            print(f"\n{community['name']}:")
            print(f"  Earnings: ${community['affiliate_earnings']}")
            print(f"  Rank: #{community['rank']}")
