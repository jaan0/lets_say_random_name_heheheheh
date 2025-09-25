import { useState, useEffect } from 'react';
import { Search, Download, CheckCircle, AlertCircle, Clock, Globe } from 'lucide-react';
import toast, { Toaster } from 'react-hot-toast';
import CookieConsent from '../components/CookieConsent';

interface AnalysisResult {
  id: string;
  url: string;
  status: string;
  progress: number;
  results?: {
    overall_score: number;
    performance: any;
    accessibility: any;
    seo: any;
    security: any;
    content: any;
  };
  error?: string;
}

export default function Home() {
  const [url, setUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [analysisId, setAnalysisId] = useState<string | null>(null);
  const [userInfo, setUserInfo] = useState({
    name: '',
    email: '',
    contact: ''
  });

  // Track user on page load
  useEffect(() => {
    // Track page visit
    if (typeof window !== 'undefined') {
      // Send page view to analytics if cookies are accepted
      const analyticsEnabled = document.cookie.includes('analytics-enabled=true');
      if (analyticsEnabled) {
        // You can add analytics tracking here
        console.log('Page view tracked');
      }
    }
  }, []);

  const startAnalysis = async () => {
    if (!url.trim()) {
      toast.error('Please enter a valid URL');
      return;
    }

    // Validate URL format
    try {
      new URL(url);
    } catch {
      toast.error('Please enter a valid URL format (e.g., https://example.com)');
      return;
    }

    setIsAnalyzing(true);
    setAnalysisResult(null);
    setAnalysisId(null);

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          url,
          name: userInfo.name,
          email: userInfo.email,
          contact: userInfo.contact
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setAnalysisId(data.analysis_id);
        toast.success('Analysis started successfully!');
        // Start polling for results
        pollAnalysisStatus(data.analysis_id);
      } else {
        toast.error(data.detail || 'Failed to start analysis');
        setIsAnalyzing(false);
      }
    } catch (error) {
      toast.error('Network error. Please try again.');
      setIsAnalyzing(false);
    }
  };

  const pollAnalysisStatus = async (id: string) => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch(`/api/analysis/${id}`);
        const data = await response.json();
        
        setAnalysisResult(data);
        
        if (data.status === 'completed') {
          setIsAnalyzing(false);
          clearInterval(pollInterval);
          toast.success('Analysis completed successfully!');
        } else if (data.status === 'failed') {
          setIsAnalyzing(false);
          clearInterval(pollInterval);
          toast.error('Analysis failed: ' + (data.error || 'Unknown error'));
        }
      } catch (error) {
        console.error('Error polling analysis status:', error);
      }
    }, 2000); // Poll every 2 seconds

    // Cleanup interval after 5 minutes
    setTimeout(() => {
      clearInterval(pollInterval);
      if (isAnalyzing) {
        setIsAnalyzing(false);
        toast.error('Analysis timeout. Please try again.');
      }
    }, 300000);
  };

  const downloadReport = async () => {
    if (!analysisId) return;

    try {
      const response = await fetch(`/api/download/${analysisId}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `website_analysis_${analysisId.slice(0, 8)}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        toast.success('Report downloaded successfully!');
      } else {
        toast.error('Failed to download report');
      }
    } catch (error) {
      toast.error('Error downloading report');
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    if (score >= 60) return 'text-orange-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 90) return 'bg-green-100';
    if (score >= 80) return 'bg-blue-100';
    if (score >= 70) return 'bg-yellow-100';
    if (score >= 60) return 'bg-orange-100';
    return 'bg-red-100';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Toaster position="top-right" />
      
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Globe className="h-8 w-8 text-blue-600" />
              <h1 className="text-2xl font-bold text-gray-900">Website Analyzer</h1>
            </div>
            <p className="text-sm text-gray-600">AI-Powered SQA Testing Tool</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Input Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Analyze Your Website
            </h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Get comprehensive insights about your website's performance, accessibility, SEO, security, and content quality. 
              Just enter your URL and get a detailed PDF report in minutes.
            </p>
          </div>

          <div className="max-w-2xl mx-auto space-y-6">
            {/* User Information (Optional) */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input
                type="text"
                value={userInfo.name}
                onChange={(e) => setUserInfo(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Your Name (Optional)"
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isAnalyzing}
              />
              <input
                type="email"
                value={userInfo.email}
                onChange={(e) => setUserInfo(prev => ({ ...prev, email: e.target.value }))}
                placeholder="Email (Optional)"
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isAnalyzing}
              />
              <input
                type="text"
                value={userInfo.contact}
                onChange={(e) => setUserInfo(prev => ({ ...prev, contact: e.target.value }))}
                placeholder="Contact (Optional)"
                className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isAnalyzing}
              />
            </div>

            {/* URL Input */}
            <div className="flex space-x-4">
              <div className="flex-1">
                <input
                  type="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                  disabled={isAnalyzing}
                />
              </div>
              <button
                onClick={startAnalysis}
                disabled={isAnalyzing || !url.trim()}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center space-x-2 text-lg font-medium"
              >
                {isAnalyzing ? (
                  <>
                    <Clock className="h-5 w-5 animate-spin" />
                    <span>Analyzing...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-5 w-5" />
                    <span>Start Analysis</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>

        {/* Progress Section */}
        {isAnalyzing && analysisResult && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h3 className="text-xl font-semibold text-gray-900 mb-4">Analysis Progress</h3>
            <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
              <div 
                className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                style={{ width: `${analysisResult.progress}%` }}
              ></div>
            </div>
            <p className="text-gray-600">
              Progress: {analysisResult.progress}% - {analysisResult.status}
            </p>
          </div>
        )}

        {/* Results Section */}
        {analysisResult && analysisResult.status === 'completed' && analysisResult.results && (
          <div className="space-y-8">
            {/* Overall Score */}
            <div className="bg-white rounded-lg shadow-lg p-8">
              <div className="text-center">
                <h3 className="text-2xl font-bold text-gray-900 mb-4">Overall Score</h3>
                <div className={`inline-flex items-center justify-center w-32 h-32 rounded-full ${getScoreBgColor(analysisResult.results.overall_score)}`}>
                  <span className={`text-4xl font-bold ${getScoreColor(analysisResult.results.overall_score)}`}>
                    {analysisResult.results.overall_score}
                  </span>
                </div>
                <p className="text-lg text-gray-600 mt-4">out of 100</p>
                <button
                  onClick={downloadReport}
                  className="mt-6 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center space-x-2 mx-auto"
                >
                  <Download className="h-5 w-5" />
                  <span>Download PDF Report</span>
                </button>
              </div>
            </div>

            {/* Category Scores */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { key: 'performance', label: 'Performance', icon: '⚡' },
                { key: 'accessibility', label: 'Accessibility', icon: '♿' },
                { key: 'seo', label: 'SEO', icon: '🔍' },
                { key: 'security', label: 'Security', icon: '🔒' },
                { key: 'content', label: 'Content', icon: '📝' }
              ].map((category) => {
                const data = analysisResult.results?.[category.key as keyof typeof analysisResult.results];
                const score = data?.score || 0;
                return (
                  <div key={category.key} className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-3">
                        <span className="text-2xl">{category.icon}</span>
                        <h4 className="text-lg font-semibold text-gray-900">{category.label}</h4>
                      </div>
                      <div className={`px-3 py-1 rounded-full ${getScoreBgColor(score)}`}>
                        <span className={`text-sm font-bold ${getScoreColor(score)}`}>
                          {score}/100
                        </span>
                      </div>
                    </div>
                    
                    {data?.issues && data.issues.length > 0 && (
                      <div className="space-y-2">
                        <p className="text-sm font-medium text-gray-700">Issues Found:</p>
                        <ul className="text-sm text-red-600 space-y-1">
                          {data.issues.slice(0, 3).map((issue: string, index: number) => (
                            <li key={index} className="flex items-start space-x-2">
                              <AlertCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                              <span>{issue}</span>
                            </li>
                          ))}
                          {data.issues.length > 3 && (
                            <li className="text-gray-500">... and {data.issues.length - 3} more</li>
                          )}
                        </ul>
                      </div>
                    )}
                    
                    {data?.recommendations && data.recommendations.length > 0 && (
                      <div className="mt-4 space-y-2">
                        <p className="text-sm font-medium text-gray-700">Top Recommendations:</p>
                        <ul className="text-sm text-blue-600 space-y-1">
                          {data.recommendations.slice(0, 2).map((rec: string, index: number) => (
                            <li key={index} className="flex items-start space-x-2">
                              <CheckCircle className="h-4 w-4 mt-0.5 flex-shrink-0" />
                              <span>{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Error Section */}
        {analysisResult && analysisResult.status === 'failed' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6">
            <div className="flex items-center space-x-3">
              <AlertCircle className="h-6 w-6 text-red-600" />
              <h3 className="text-lg font-semibold text-red-800">Analysis Failed</h3>
            </div>
            <p className="text-red-700 mt-2">{analysisResult.error}</p>
            <button
              onClick={() => {
                setAnalysisResult(null);
                setAnalysisId(null);
                setIsAnalyzing(false);
              }}
              className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
            >
              Try Again
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-600">
            <p>&copy; 2024 Website Analyzer. AI-Powered SQA Testing Tool.</p>
          </div>
        </div>
      </footer>

      {/* Cookie Consent */}
      <CookieConsent />
    </div>
  );
}
