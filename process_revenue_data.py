from scrape_affiliate_revenue import scrape_affiliate_revenue
from typing import List, Dict
import re
import os
import json

def process_revenue_data() -> Dict:
    """Process scraped revenue data into final combined format"""
    raw_data = scrape_affiliate_revenue()
    
    if raw_data is None:
        data_path = os.path.join(os.path.dirname(__file__), 'data', 'scraped_data.json')
        try:
            with open(data_path, 'r') as f:
                raw_data = json.load(f)
        except Exception as e:
            print(f"Error loading saved data: {e}")
            return {}

    combined_data = {
        "platform_metrics": raw_data.get("platform_metrics", {}),
        "top_communities": []
    }

    # Get raw data lists
    earnings = raw_data.get("affiliate_earnings", [])
    communities = raw_data.get("top_communities", [])
    
    # Merge communities with their earnings and add rank
    for idx, community in enumerate(communities):
        if idx < len(earnings):
            community_copy = dict(community)
            community_copy["affiliate_earnings"] = earnings[idx]
            community_copy["rank"] = idx + 1
            combined_data["top_communities"].append(community_copy)
    
    # Save combined data
    output_path = os.path.join(os.path.dirname(__file__), 'data', 'combined_data.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(combined_data, f, indent=2)
        print(f"Combined data saved to {output_path}")

    return combined_data

if __name__ == "__main__":
    process_revenue_data()
