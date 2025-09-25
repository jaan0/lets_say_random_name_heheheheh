import axios from 'axios';
import * as cheerio from 'cheerio';

class WebsiteAnalyzer {
  constructor() {
    this.timeout = 30000; // 30 seconds timeout
  }

  async analyzePerformance(url) {
    try {
      const startTime = Date.now();
      
      // Basic performance metrics
      const response = await axios.get(url, { 
        timeout: this.timeout,
        validateStatus: () => true // Accept any status code
      });
      
      const loadTime = Date.now() - startTime;
      const contentSize = Buffer.byteLength(response.data, 'utf8');
      
      // Parse HTML for additional metrics
      const $ = cheerio.load(response.data);
      const images = $('img').length;
      const scripts = $('script').length;
      const stylesheets = $('link[rel="stylesheet"]').length;
      
      // Calculate performance score
      const score = this.calculatePerformanceScore(loadTime, contentSize, response.status);
      
      return {
        load_time: loadTime,
        page_size: contentSize,
        status_code: response.status,
        images_count: images,
        scripts_count: scripts,
        stylesheets_count: stylesheets,
        score: score,
        headers: response.headers
      };
    } catch (error) {
      return {
        error: error.message,
        score: 0
      };
    }
  }

  async analyzeAccessibility(url) {
    try {
      const response = await axios.get(url, { timeout: this.timeout });
      const $ = cheerio.load(response.data);
      
      let issues = [];
      let score = 100;
      
      // Check for alt attributes on images
      const imagesWithoutAlt = $('img:not([alt])').length;
      if (imagesWithoutAlt > 0) {
        issues.push(`${imagesWithoutAlt} images missing alt attributes`);
        score -= imagesWithoutAlt * 5;
      }
      
      // Check for heading structure
      const headings = $('h1, h2, h3, h4, h5, h6');
      const h1Count = $('h1').length;
      if (h1Count === 0) {
        issues.push('No H1 heading found');
        score -= 20;
      } else if (h1Count > 1) {
        issues.push('Multiple H1 headings found');
        score -= 10;
      }
      
      // Check for form labels
      const inputsWithoutLabels = $('input:not([aria-label]):not([aria-labelledby])').filter(function() {
        return !$(this).closest('label').length;
      }).length;
      if (inputsWithoutLabels > 0) {
        issues.push(`${inputsWithoutLabels} form inputs missing labels`);
        score -= inputsWithoutLabels * 10;
      }
      
      // Check for color contrast (basic check)
      const hasColorContrast = $('*[style*="color"]').length > 0;
      if (!hasColorContrast) {
        issues.push('No explicit color contrast found');
        score -= 5;
      }
      
      return {
        score: Math.max(0, score),
        issues: issues,
        total_issues: issues.length,
        images_without_alt: imagesWithoutAlt,
        h1_count: h1Count,
        inputs_without_labels: inputsWithoutLabels
      };
    } catch (error) {
      return {
        error: error.message,
        score: 0
      };
    }
  }

  async analyzeSEO(url) {
    try {
      const response = await axios.get(url, { timeout: this.timeout });
      const $ = cheerio.load(response.data);
      
      let score = 100;
      let issues = [];
      
      // Check title tag
      const title = $('title').text().trim();
      if (!title) {
        issues.push('Missing title tag');
        score -= 25;
      } else if (title.length < 30 || title.length > 60) {
        issues.push('Title length should be 30-60 characters');
        score -= 10;
      }
      
      // Check meta description
      const metaDescription = $('meta[name="description"]').attr('content');
      if (!metaDescription) {
        issues.push('Missing meta description');
        score -= 20;
      } else if (metaDescription.length < 120 || metaDescription.length > 160) {
        issues.push('Meta description should be 120-160 characters');
        score -= 10;
      }
      
      // Check for H1 tag
      const h1Count = $('h1').length;
      if (h1Count === 0) {
        issues.push('Missing H1 tag');
        score -= 15;
      }
      
      // Check for meta keywords (optional but good to have)
      const metaKeywords = $('meta[name="keywords"]').attr('content');
      if (!metaKeywords) {
        issues.push('Missing meta keywords');
        score -= 5;
      }
      
      // Check for canonical URL
      const canonical = $('link[rel="canonical"]').attr('href');
      if (!canonical) {
        issues.push('Missing canonical URL');
        score -= 10;
      }
      
      // Check for Open Graph tags
      const ogTitle = $('meta[property="og:title"]').attr('content');
      const ogDescription = $('meta[property="og:description"]').attr('content');
      if (!ogTitle || !ogDescription) {
        issues.push('Missing Open Graph tags');
        score -= 10;
      }
      
      return {
        score: Math.max(0, score),
        issues: issues,
        total_issues: issues.length,
        title: title,
        meta_description: metaDescription,
        h1_count: h1Count,
        has_canonical: !!canonical,
        has_og_tags: !!(ogTitle && ogDescription)
      };
    } catch (error) {
      return {
        error: error.message,
        score: 0
      };
    }
  }

  async analyzeSecurity(url) {
    try {
      const response = await axios.get(url, { timeout: this.timeout });
      const $ = cheerio.load(response.data);
      
      let score = 100;
      let issues = [];
      
      // Check for HTTPS
      if (!url.startsWith('https://')) {
        issues.push('Site not using HTTPS');
        score -= 30;
      }
      
      // Check for security headers
      const headers = response.headers;
      if (!headers['x-frame-options']) {
        issues.push('Missing X-Frame-Options header');
        score -= 10;
      }
      if (!headers['x-content-type-options']) {
        issues.push('Missing X-Content-Type-Options header');
        score -= 10;
      }
      if (!headers['x-xss-protection']) {
        issues.push('Missing X-XSS-Protection header');
        score -= 10;
      }
      if (!headers['strict-transport-security']) {
        issues.push('Missing Strict-Transport-Security header');
        score -= 15;
      }
      
      // Check for mixed content
      const httpResources = $('img[src^="http:"], script[src^="http:"], link[href^="http:"]').length;
      if (httpResources > 0) {
        issues.push(`${httpResources} HTTP resources found (mixed content)`);
        score -= httpResources * 5;
      }
      
      // Check for inline scripts (potential XSS risk)
      const inlineScripts = $('script:not([src])').length;
      if (inlineScripts > 0) {
        issues.push(`${inlineScripts} inline scripts found`);
        score -= inlineScripts * 2;
      }
      
      return {
        score: Math.max(0, score),
        issues: issues,
        total_issues: issues.length,
        is_https: url.startsWith('https://'),
        security_headers: {
          x_frame_options: !!headers['x-frame-options'],
          x_content_type_options: !!headers['x-content-type-options'],
          x_xss_protection: !!headers['x-xss-protection'],
          strict_transport_security: !!headers['strict-transport-security']
        },
        http_resources: httpResources,
        inline_scripts: inlineScripts
      };
    } catch (error) {
      return {
        error: error.message,
        score: 0
      };
    }
  }

  async analyzeContent(url) {
    try {
      const response = await axios.get(url, { timeout: this.timeout });
      const $ = cheerio.load(response.data);
      
      // Remove script and style elements
      $('script, style').remove();
      
      const text = $('body').text().trim();
      const wordCount = text.split(/\s+/).length;
      const headingCount = $('h1, h2, h3, h4, h5, h6').length;
      const paragraphCount = $('p').length;
      const linkCount = $('a').length;
      const imageCount = $('img').length;
      
      // Calculate content score
      let score = 100;
      let issues = [];
      
      if (wordCount < 300) {
        issues.push('Content too short (less than 300 words)');
        score -= 20;
      }
      
      if (headingCount === 0) {
        issues.push('No headings found');
        score -= 15;
      }
      
      if (paragraphCount === 0) {
        issues.push('No paragraphs found');
        score -= 10;
      }
      
      if (linkCount === 0) {
        issues.push('No links found');
        score -= 5;
      }
      
      return {
        score: Math.max(0, score),
        issues: issues,
        total_issues: issues.length,
        word_count: wordCount,
        heading_count: headingCount,
        paragraph_count: paragraphCount,
        link_count: linkCount,
        image_count: imageCount,
        content_length: text.length
      };
    } catch (error) {
      return {
        error: error.message,
        score: 0
      };
    }
  }

  calculatePerformanceScore(loadTime, contentSize, statusCode) {
    let score = 100;
    
    // Penalize slow load times
    if (loadTime > 3000) score -= 30;
    else if (loadTime > 2000) score -= 20;
    else if (loadTime > 1000) score -= 10;
    
    // Penalize large content
    if (contentSize > 1000000) score -= 20; // > 1MB
    else if (contentSize > 500000) score -= 10; // > 500KB
    
    // Penalize non-200 status codes
    if (statusCode !== 200) score -= 25;
    
    return Math.max(0, score);
  }

  calculateOverallScore(performance, accessibility, seo, security, content) {
    const scores = [];
    if (performance && performance.score !== undefined) scores.push(performance.score);
    if (accessibility && accessibility.score !== undefined) scores.push(accessibility.score);
    if (seo && seo.score !== undefined) scores.push(seo.score);
    if (security && security.score !== undefined) scores.push(security.score);
    if (content && content.score !== undefined) scores.push(content.score);
    
    return scores.length > 0 ? Math.round(scores.reduce((a, b) => a + b, 0) / scores.length) : 0;
  }
}

export default WebsiteAnalyzer;
