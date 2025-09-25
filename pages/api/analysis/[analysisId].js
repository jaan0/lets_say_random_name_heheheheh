import AnalysisStorage from '../../../lib/storage.js';

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

    res.status(200).json(result);

  } catch (error) {
    console.error('Error in analysis status endpoint:', error);
    res.status(500).json({ error: error.message });
  }
}
