import { exec } from 'child_process'
import { promisify } from 'util'
import { saveWhopData } from './db'
import { readFileSync } from 'fs'
import { join } from 'path'

const execAsync = promisify(exec)

export default async function handler(req, res) {
  try {
    if (!req.headers['x-vercel-cron'] && process.env.NODE_ENV === 'production') {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    const { stdout } = await execAsync('python process_revenue_data.py')
    
    const dataPath = join(process.cwd(), 'data', 'combined_data.json')
    const whopData = JSON.parse(readFileSync(dataPath, 'utf8'))
    await saveWhopData(whopData)
    
    return res.status(200).json({
      message: 'Data updated successfully',
      stdout
    })
  } catch (error) {
    return res.status(500).json({ error: 'Failed to update data' })
  }
}