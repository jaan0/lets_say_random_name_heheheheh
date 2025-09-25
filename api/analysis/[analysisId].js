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

    // For now, return a mock result
    // In a real implementation, you would retrieve this from a database
    const mockResult = {
      id: analysisId,
      url: 'https://example.com',
      status: 'completed',
      started_at: new Date().toISOString(),
      progress: 100,
      results: {
        overall_score: 85,
        performance: { score: 80 },
        accessibility: { score: 90 },
        seo: { score: 85 }
      },
      error: null
    };

    res.status(200).json(mockResult);

  } catch (error) {
    console.error('Error in analysis status endpoint:', error);
    res.status(500).json({ error: error.message });
  }
}
