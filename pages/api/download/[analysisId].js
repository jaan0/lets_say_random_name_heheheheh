import AnalysisStorage from '../../../lib/storage.js';
import fs from 'fs';
import path from 'path';

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow GET requests
  if (req.method !== 'GET') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const { analysisId } = req.query;

    if (!analysisId) {
      res.status(400).json({ error: 'Analysis ID is required' });
      return;
    }

    const storage = new AnalysisStorage();
    const result = storage.getAnalysisResult(analysisId);

    if (!result) {
      res.status(404).json({ error: 'Analysis not found' });
      return;
    }

    if (result.status !== 'completed') {
      res.status(400).json({ error: 'Analysis not completed yet' });
      return;
    }

    // Check if PDF file exists
    const pdfPath = path.join(process.cwd(), 'api', 'reports', `${analysisId}.pdf`);
    
    if (!fs.existsSync(pdfPath)) {
      res.status(404).json({ error: 'Report file not found' });
      return;
    }

    // Set headers for file download
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename="website_analysis_${analysisId.slice(0, 8)}.pdf"`);

    // Stream the file
    const fileStream = fs.createReadStream(pdfPath);
    fileStream.pipe(res);

  } catch (error) {
    console.error('Error in download endpoint:', error);
    res.status(500).json({ error: error.message });
  }
}
