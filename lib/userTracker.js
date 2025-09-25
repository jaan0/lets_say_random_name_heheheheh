import { SupabaseDB } from './supabase.js';

export class UserTracker {
  constructor() {
    this.db = new SupabaseDB();
  }

  // Get user IP address from request
  getClientIP(req) {
    const forwarded = req.headers['x-forwarded-for'];
    const realIP = req.headers['x-real-ip'];
    const cfConnectingIP = req.headers['cf-connecting-ip'];
    
    if (cfConnectingIP) return cfConnectingIP;
    if (realIP) return realIP;
    if (forwarded) return forwarded.split(',')[0].trim();
    
    return req.connection?.remoteAddress || 
           req.socket?.remoteAddress || 
           req.ip || 
           '127.0.0.1';
  }

  // Get user agent information
  getUserAgentInfo(req) {
    const userAgent = req.headers['user-agent'] || '';
    
    // Basic browser detection
    let browser = 'Unknown';
    let os = 'Unknown';
    
    if (userAgent.includes('Chrome')) browser = 'Chrome';
    else if (userAgent.includes('Firefox')) browser = 'Firefox';
    else if (userAgent.includes('Safari')) browser = 'Safari';
    else if (userAgent.includes('Edge')) browser = 'Edge';
    
    if (userAgent.includes('Windows')) os = 'Windows';
    else if (userAgent.includes('Mac')) os = 'macOS';
    else if (userAgent.includes('Linux')) os = 'Linux';
    else if (userAgent.includes('Android')) os = 'Android';
    else if (userAgent.includes('iOS')) os = 'iOS';
    
    return {
      userAgent,
      browser,
      os,
      isMobile: /Mobile|Android|iPhone|iPad/.test(userAgent)
    };
  }

  // Get location information (basic)
  getLocationInfo(req) {
    const country = req.headers['cf-ipcountry'] || 
                   req.headers['x-country-code'] || 
                   'Unknown';
    
    const city = req.headers['cf-ipcity'] || 
                 req.headers['x-city'] || 
                 'Unknown';
    
    return { country, city };
  }

  // Track user session
  async trackUser(req, additionalData = {}) {
    try {
      const ipAddress = this.getClientIP(req);
      const userAgentInfo = this.getUserAgentInfo(req);
      const locationInfo = this.getLocationInfo(req);
      
      const userData = {
        ip_address: ipAddress,
        user_agent: userAgentInfo.userAgent,
        browser: userAgentInfo.browser,
        operating_system: userAgentInfo.os,
        is_mobile: userAgentInfo.isMobile,
        country: locationInfo.country,
        city: locationInfo.city,
        last_seen: new Date().toISOString(),
        ...additionalData
      };

      // Save or update user
      const user = await this.db.saveUser(userData);
      return user;
    } catch (error) {
      console.error('Error tracking user:', error);
      return null;
    }
  }

  // Track analysis request
  async trackAnalysis(analysisId, url, userId, req) {
    try {
      const ipAddress = this.getClientIP(req);
      const userAgentInfo = this.getUserAgentInfo(req);
      
      const analysisData = {
        id: analysisId,
        user_id: userId,
        url: url,
        ip_address: ipAddress,
        user_agent: userAgentInfo.userAgent,
        browser: userAgentInfo.browser,
        operating_system: userAgentInfo.os,
        is_mobile: userAgentInfo.isMobile,
        status: 'started',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      const result = await this.db.saveAnalysis(analysisData);
      return result;
    } catch (error) {
      console.error('Error tracking analysis:', error);
      return null;
    }
  }

  // Update analysis with results
  async updateAnalysis(analysisId, results, pdfPath) {
    try {
      const updateData = {
        status: 'completed',
        results: results,
        pdf_path: pdfPath,
        overall_score: results.overall_score,
        updated_at: new Date().toISOString()
      };

      const { data, error } = await this.db.client
        .from('analyses')
        .update(updateData)
        .eq('id', analysisId)
        .select()
        .single();

      if (error) {
        console.error('Error updating analysis:', error);
        return null;
      }

      return data;
    } catch (error) {
      console.error('Error updating analysis:', error);
      return null;
    }
  }

  // Get user analytics
  async getUserAnalytics(userId) {
    try {
      return await this.db.getUserAnalyses(userId);
    } catch (error) {
      console.error('Error getting user analytics:', error);
      return [];
    }
  }
}

export default UserTracker;
