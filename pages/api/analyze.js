import WebsiteAnalyzer from '../../lib/analyzer.js';
import AnalysisStorage from '../../lib/storage.js';
import PDFReportGenerator from '../../lib/reportGenerator.js';
import UserTracker from '../../lib/userTracker.js';

export default async function handler(req, res) {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  // Only allow POST requests
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  try {
    const { url, options = {} } = req.body;

    if (!url) {
      res.status(400).json({ error: 'URL is required' });
      return;
    }

    // Generate analysis ID
    const analysisId = crypto.randomUUID();
    const storage = new AnalysisStorage();
    const analyzer = new WebsiteAnalyzer();
    const userTracker = new UserTracker();

    // Track user and get user info (optional)
    let user = null;
    try {
      user = await userTracker.trackUser(req, {
        name: req.body.name || null,
        email: req.body.email || null,
        contact: req.body.contact || null
      });
    } catch (error) {
      console.log('User tracking failed (optional):', error.message);
    }

    // Initialize analysis result
    const initialResult = {
      id: analysisId,
      url: url,
      status: 'started',
      started_at: new Date().toISOString(),
      progress: 0,
      results: null,
      error: null,
      user_id: user?.id || null
    };

    // Save initial result to local storage
    storage.saveAnalysisResult(analysisId, initialResult);
    
    // Track analysis in Supabase (optional)
    try {
      await userTracker.trackAnalysis(analysisId, url, user?.id, req);
    } catch (error) {
      console.log('Analysis tracking failed (optional):', error.message);
    }

    // Start analysis in background (simplified for serverless)
    try {
      // Update status to analyzing
      initialResult.status = 'analyzing';
      initialResult.progress = 10;
      storage.saveAnalysisResult(analysisId, initialResult);

      // Run analysis steps
      initialResult.progress = 20;
      storage.saveAnalysisResult(analysisId, initialResult);
      const performanceData = await analyzer.analyzePerformance(url);

      initialResult.progress = 40;
      storage.saveAnalysisResult(analysisId, initialResult);
      const accessibilityData = await analyzer.analyzeAccessibility(url);

      initialResult.progress = 60;
      storage.saveAnalysisResult(analysisId, initialResult);
      const seoData = await analyzer.analyzeSEO(url);

      initialResult.progress = 80;
      storage.saveAnalysisResult(analysisId, initialResult);
      const securityData = await analyzer.analyzeSecurity(url);

      initialResult.progress = 90;
      storage.saveAnalysisResult(analysisId, initialResult);
      const contentData = await analyzer.analyzeContent(url);

      // Compile results
      const results = {
        url: url,
        analyzed_at: new Date().toISOString(),
        performance: performanceData,
        accessibility: accessibilityData,
        seo: seoData,
        security: securityData,
        content: contentData,
        overall_score: analyzer.calculateOverallScore(performanceData, accessibilityData, seoData, securityData, contentData)
      };

      initialResult.results = results;
      initialResult.progress = 95;
      storage.saveAnalysisResult(analysisId, initialResult);

      // Generate PDF report
      const reportGenerator = new PDFReportGenerator();
      const pdfBase64 = reportGenerator.generateReport(results, analysisId);

      initialResult.status = 'completed';
      initialResult.progress = 100;
      initialResult.pdf_base64 = pdfBase64;
      storage.saveAnalysisResult(analysisId, initialResult);

      // Update analysis in Supabase with results (optional)
      try {
        await userTracker.updateAnalysis(analysisId, results, pdfBase64);
      } catch (error) {
        console.log('Analysis update failed (optional):', error.message);
      }

    } catch (analysisError) {
      // Update result with error
      initialResult.status = 'failed';
      initialResult.error = analysisError.message;
      storage.saveAnalysisResult(analysisId, initialResult);
    }

    res.status(200).json({
      analysis_id: analysisId,
      status: 'started',
      message: 'Analysis started successfully',
      url: url
    });

  } catch (error) {
    console.error('Error in analyze endpoint:', error);
    res.status(500).json({ error: error.message });
  }
}
