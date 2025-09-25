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

  try {
    const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
    const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
    
    const debugInfo = {
      supabase_configured: !!(supabaseUrl && supabaseKey && 
        supabaseUrl !== 'your-supabase-url' && 
        supabaseKey !== 'your-supabase-anon-key'),
      supabase_url: supabaseUrl ? 'Set' : 'Not set',
      supabase_key: supabaseKey ? 'Set' : 'Not set',
      environment: process.env.NODE_ENV,
      timestamp: new Date().toISOString()
    };

    // Test Supabase connection if configured
    if (debugInfo.supabase_configured) {
      try {
        const { createClient } = await import('@supabase/supabase-js');
        const supabase = createClient(supabaseUrl, supabaseKey);
        
        // Test connection
        const { data, error } = await supabase
          .from('analyses')
          .select('count')
          .limit(1);
        
        debugInfo.supabase_connection = error ? 'Failed' : 'Success';
        debugInfo.supabase_error = error?.message || null;
      } catch (error) {
        debugInfo.supabase_connection = 'Failed';
        debugInfo.supabase_error = error.message;
      }
    }

    res.status(200).json(debugInfo);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
