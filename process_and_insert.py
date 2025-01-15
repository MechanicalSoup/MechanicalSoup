import json
import os
import re
from dotenv import load_dotenv
from scrape_affiliate_revenue import scrape_affiliate_revenue
from prisma import Prisma
import asyncio

# Load environment variables
load_dotenv()

def clean_monetary_value(value: str) -> float:
    """Convert string monetary values to float"""
    if isinstance(value, (int, float)):
        return float(value)
    return float(re.sub(r'[^\d.]', '', value))

def process_revenue_data(raw_data):
    """Process scraped revenue data"""
    clean_data = {
        "platform_metrics": {
            "total_revenue": None,
            "total_users": None
        },
        "affiliate_earnings": set(),
        "products": []
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

    # Handle products
    clean_data["products"] = raw_data.get("products", [])

    return {
        "platform_metrics": clean_data["platform_metrics"],
        "affiliate_earnings": sorted(list(clean_data["affiliate_earnings"]), reverse=True),
        "products": clean_data["products"]
    }

async def run_and_insert_data():
    """Run scraper and insert data into database"""
    db = Prisma()
    await db.connect()
    
    try:
        raw_data = scrape_affiliate_revenue()
        cleaned_data = process_revenue_data(raw_data)
        
        # Insert platform metrics
        await db.metrics.create(
            data={
                'totalRevenue': cleaned_data['platform_metrics']['total_revenue'],
                'totalUsers': cleaned_data['platform_metrics']['total_users']
            }
        )

        # Insert earnings
        for earning in cleaned_data['affiliate_earnings']:
            await db.earnings.create(
                data={
                    'value': earning
                }
            )

        # Insert products
        for product in cleaned_data['products']:
            await db.products.create(
                data={
                    'name': product['name'],
                    'text_medium': product['text_medium'],
                    'price': product['price'],
                    'time_range': product['time_range'],
                    'whop_rank': product['whop_rank'],
                    'logo': product['logo']
                }
            )
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(run_and_insert_data())
