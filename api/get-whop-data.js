import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default async function handler(req, res) {
  try {
    // Add domain-specific CORS
    res.setHeader('Access-Control-Allow-Origin', 'https://inforadar.io');
    res.setHeader('Access-Control-Allow-Credentials', true);
    res.setHeader('Access-Control-Allow-Methods', 'GET');
    res.setHeader('Cache-Control', 's-maxage=86400'); // Cache for 24 hours

    const dataPath = join(__dirname, '..', 'data', 'combined_data.json');
    const whopData = JSON.parse(readFileSync(dataPath, 'utf8'));

    return res.status(200).json(whopData);
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ 
      error: 'Failed to load data',
      details: error.message 
    });
  }
}
