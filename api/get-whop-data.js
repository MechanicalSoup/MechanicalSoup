import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import cors from 'cors';
import { getLatestWhopData } from './db'

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default async function handler(req, res) {
  // Enable CORS
  await cors()(req, res);

  try {
    const whopData = await getLatestWhopData()
    
    if (!whopData) {
      return res.status(404).json({ error: 'No data found' })
    }

    const formattedData = {
      platform_metrics: {
        total_revenue: whopData.totalRevenue,
        total_users: whopData.totalUsers
      },
      top_communities: whopData.communities.map(c => ({
        name: c.name,
        price_per_unit: c.pricePerUnit,
        logo: c.logo,
        title: c.title,
        other_information: c.otherInformation,
        whop_rank: c.whopRank,
        affiliate_earnings: c.affiliateEarnings,
        rank: c.rank
      }))
    }

    res.setHeader('Access-Control-Allow-Origin', 'https://inforadar.io')
    res.setHeader('Cache-Control', 's-maxage=86400')
    return res.status(200).json(formattedData)
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ 
      error: 'Failed to load data'
    });
  }
}
