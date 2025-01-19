import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import type { VercelRequest, VercelResponse } from '@vercel/node';
import type { WhopData } from '../types/whop';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default async function handler(
  req: VercelRequest, 
  res: VercelResponse
) {
  try {
    // ...existing CORS headers...

    const dataPath = join(__dirname, '..', 'data', 'combined_data.json');
    const whopData: WhopData = JSON.parse(readFileSync(dataPath, 'utf8'));

    return res.status(200).json(whopData);
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({ 
      error: 'Failed to load data',
      details: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
