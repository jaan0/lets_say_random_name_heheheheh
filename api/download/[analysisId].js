import fs from 'fs';
import AnalysisStorage from '../../../lib/storage.js';

export default function handler(req, res) {
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

    // Get analysis result from storage
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
    const pdfPath = `/tmp/reports/${analysisId}.pdf`;
    if (!fs.existsSync(pdfPath)) {
      res.status(404).json({ error: 'Report file not found' });
      return;
    }

    // Read and return the PDF file
    const pdfBuffer = fs.readFileSync(pdfPath);
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename=website_analysis_${analysisId.substring(0, 8)}.pdf`);
    res.setHeader('Content-Length', pdfBuffer.length);
    
    res.status(200).send(pdfBuffer);

  } catch (error) {
    console.error('Error in download endpoint:', error);
    res.status(500).json({ error: error.message });
  }
}
