import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export default async function handler(req, res) {
  try {
    // Only allow scheduled jobs or authenticated requests
    if (!req.headers['x-vercel-cron'] && process.env.NODE_ENV === 'production') {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // Run the Python script
    const { stdout, stderr } = await execAsync('python process_revenue_data.py');
    
    return res.status(200).json({
      message: 'Data updated successfully',
      stdout,
      stderr
    });
  } catch (error) {
    return res.status(500).json({ 
      error: 'Failed to update data',
      details: error.message 
    });
  }
}