import json
import os
from typing import Dict, List

def clean_whop_rank(rank: str) -> int:
    """Convert whop rank string to integer for sorting"""
    return int(rank.replace('#', ''))

def combine_and_sort_data():
    """Combine scraped data and sort by affiliate earnings"""
    input_path = os.path.join('data', 'scraped_data.json')
    output_path = os.path.join('data', 'combined_data.json')
    
    try:
        # Load scraped data
        with open(input_path, 'r') as f:
            data = json.load(f)
            
        # Get the lists to combine
        earnings = data.get('affiliate_earnings', [])
        communities = data.get('top_communities', [])
        
        # Combine data
        combined_communities = []
        for idx, community in enumerate(communities):
            if idx < len(earnings):
                combined_communities.append({
                    **community,
                    "affiliate_earnings": earnings[idx],
                    "affiliate_earnings_value": float(earnings[idx].replace(',', '')),
                    "rank": idx + 1
                })
        
        # Sort by affiliate earnings
        sorted_communities = sorted(
            combined_communities,
            key=lambda x: x['affiliate_earnings_value'],
            reverse=True
        )
        
        # Remove the sorting value from final output
        for community in sorted_communities:
            del community['affiliate_earnings_value']
        
        # Prepare final output
        final_data = {
            "platform_metrics": data['platform_metrics'],
            "top_communities": sorted_communities
        }
        
        # Save combined and sorted data
        with open(output_path, 'w') as f:
            json.dump(final_data, f, indent=2)
            print(f"Combined data saved to {output_path}")
        
        return final_data
            
    except Exception as e:
        print(f"Error combining data: {e}")
        return None

if __name__ == "__main__":
    result = combine_and_sort_data()
    if result:
        print("\nCombined and sorted successfully!")
        print(f"Found {len(result['top_communities'])} communities")
        print("\nTop 3 communities by earnings:")
        for community in result['top_communities'][:3]:
            print(f"{community['name']}: ${community['affiliate_earnings']}")
