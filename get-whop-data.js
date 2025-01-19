import { readFileSync } from 'fs';
import { join } from 'path';
import express from 'express';
import cors from 'cors';

const app = express();
app.use(cors());

// Serve the Whop data endpoint
app.get('/api/whop-data', (req, res) => {
    try {
        const dataPath = join(process.cwd(), 'data', 'combined_data.json');
        const whopData = JSON.parse(readFileSync(dataPath, 'utf8'));
        
        res.setHeader('Cache-Control', 's-maxage=86400');
        res.json(whopData);
    } catch (error) {
        res.status(500).json({ 
            error: 'Failed to load Whop data',
            details: error.message 
        });
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});

export default app;
