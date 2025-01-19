import express from 'express';
import cors from 'cors';
import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
app.use(cors());

// Serve the Whop data endpoint
app.get('/api/whop-data', (req, res) => {
    try {
        const dataPath = join(__dirname, 'data', 'combined_data.json');
        const whopData = JSON.parse(readFileSync(dataPath, 'utf8'));
        
        res.json(whopData);
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to load Whop data',
            details: error.message 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
