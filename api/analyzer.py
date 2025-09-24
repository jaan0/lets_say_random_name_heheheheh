import asyncio
import aiohttp
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from typing import Dict, List, Any
import time

class WebsiteAnalyzer:
    def __init__(self):
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def analyze_performance(self, url: str) -> Dict[str, Any]:
        """Analyze website performance metrics"""
        try:
            start_time = time.time()
            
            async with aiohttp.ClientSession() as session:
                # Measure page load time
                async with session.get(url, timeout=30) as response:
                    load_time = time.time() - start_time
                    content = await response.text()
                    content_size = len(content.encode('utf-8'))
                    
                    # Basic performance metrics
                    performance_data = {
                        "load_time": round(load_time, 2),
                        "page_size": content_size,
                        "status_code": response.status,
                        "headers": dict(response.headers),
                        "score": self._calculate_performance_score(load_time, content_size, response.status)
                    }
                    
                    # Analyze images
                    soup = BeautifulSoup(content, 'html.parser')
                    images = soup.find_all('img')
                    total_image_size = 0
                    unoptimized_images = 0
                    
                    for img in images:
                        if img.get('src'):
                            img_url = urljoin(url, img['src'])
                            try:
                                async with session.head(img_url, timeout=10) as img_response:
                                    img_size = int(img_response.headers.get('content-length', 0))
                                    total_image_size += img_size
                                    if img_size > 100000:  # > 100KB
                                        unoptimized_images += 1
                            except:
                                pass
                    
                    performance_data.update({
                        "total_images": len(images),
                        "total_image_size": total_image_size,
                        "unoptimized_images": unoptimized_images,
                        "recommendations": self._get_performance_recommendations(load_time, content_size, unoptimized_images)
                    })
                    
                    return performance_data
                    
        except Exception as e:
            return {"error": str(e), "score": 0}
    
    async def analyze_accessibility(self, url: str) -> Dict[str, Any]:
        """Analyze website accessibility"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Accessibility checks
                    issues = []
                    score = 100
                    
                    # Check for alt text on images
                    images_without_alt = soup.find_all('img', alt='')
                    if images_without_alt:
                        issues.append(f"Found {len(images_without_alt)} images without alt text")
                        score -= len(images_without_alt) * 2
                    
                    # Check for heading structure
                    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    h1_count = len(soup.find_all('h1'))
                    if h1_count == 0:
                        issues.append("No H1 heading found")
                        score -= 10
                    elif h1_count > 1:
                        issues.append(f"Multiple H1 headings found ({h1_count})")
                        score -= 5
                    
                    # Check for form labels
                    inputs = soup.find_all('input')
                    inputs_without_labels = 0
                    for input_tag in inputs:
                        if input_tag.get('type') not in ['hidden', 'submit', 'button']:
                            if not input_tag.get('aria-label') and not input_tag.get('aria-labelledby'):
                                # Check if there's a label associated
                                input_id = input_tag.get('id')
                                if input_id:
                                    label = soup.find('label', {'for': input_id})
                                    if not label:
                                        inputs_without_labels += 1
                    
                    if inputs_without_labels > 0:
                        issues.append(f"Found {inputs_without_labels} form inputs without proper labels")
                        score -= inputs_without_labels * 3
                    
                    # Check for color contrast (basic check)
                    style_tags = soup.find_all('style')
                    inline_styles = soup.find_all(attrs={'style': True})
                    if not style_tags and not inline_styles:
                        issues.append("No CSS found - color contrast cannot be verified")
                        score -= 5
                    
                    return {
                        "score": max(0, score),
                        "issues": issues,
                        "total_issues": len(issues),
                        "recommendations": self._get_accessibility_recommendations(issues)
                    }
                    
        except Exception as e:
            return {"error": str(e), "score": 0}
    
    async def analyze_seo(self, url: str) -> Dict[str, Any]:
        """Analyze SEO aspects"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    seo_data = {"score": 100, "issues": [], "recommendations": []}
                    
                    # Check title tag
                    title = soup.find('title')
                    if not title or not title.get_text().strip():
                        seo_data["issues"].append("Missing or empty title tag")
                        seo_data["score"] -= 20
                    else:
                        title_text = title.get_text().strip()
                        if len(title_text) < 30:
                            seo_data["issues"].append("Title tag is too short (less than 30 characters)")
                            seo_data["score"] -= 5
                        elif len(title_text) > 60:
                            seo_data["issues"].append("Title tag is too long (more than 60 characters)")
                            seo_data["score"] -= 5
                    
                    # Check meta description
                    meta_desc = soup.find('meta', attrs={'name': 'description'})
                    if not meta_desc or not meta_desc.get('content', '').strip():
                        seo_data["issues"].append("Missing meta description")
                        seo_data["score"] -= 15
                    else:
                        desc_text = meta_desc.get('content', '').strip()
                        if len(desc_text) < 120:
                            seo_data["issues"].append("Meta description is too short (less than 120 characters)")
                            seo_data["score"] -= 5
                        elif len(desc_text) > 160:
                            seo_data["issues"].append("Meta description is too long (more than 160 characters)")
                            seo_data["score"] -= 5
                    
                    # Check for H1 tag
                    h1_tags = soup.find_all('h1')
                    if len(h1_tags) == 0:
                        seo_data["issues"].append("No H1 tag found")
                        seo_data["score"] -= 10
                    elif len(h1_tags) > 1:
                        seo_data["issues"].append("Multiple H1 tags found")
                        seo_data["score"] -= 5
                    
                    # Check for images without alt text
                    images = soup.find_all('img')
                    images_without_alt = [img for img in images if not img.get('alt')]
                    if images_without_alt:
                        seo_data["issues"].append(f"Found {len(images_without_alt)} images without alt text")
                        seo_data["score"] -= len(images_without_alt) * 2
                    
                    # Check for internal links
                    links = soup.find_all('a', href=True)
                    internal_links = 0
                    for link in links:
                        href = link['href']
                        if href.startswith('/') or urlparse(href).netloc == urlparse(url).netloc:
                            internal_links += 1
                    
                    if internal_links < 3:
                        seo_data["issues"].append("Very few internal links found")
                        seo_data["score"] -= 5
                    
                    # Check for structured data
                    json_ld = soup.find_all('script', type='application/ld+json')
                    if not json_ld:
                        seo_data["issues"].append("No structured data (JSON-LD) found")
                        seo_data["score"] -= 10
                    
                    seo_data["total_issues"] = len(seo_data["issues"])
                    seo_data["recommendations"] = self._get_seo_recommendations(seo_data["issues"])
                    
                    return seo_data
                    
        except Exception as e:
            return {"error": str(e), "score": 0}
    
    async def analyze_security(self, url: str) -> Dict[str, Any]:
        """Analyze basic security aspects"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    security_data = {"score": 100, "issues": [], "recommendations": []}
                    
                    # Check HTTPS
                    if not url.startswith('https://'):
                        security_data["issues"].append("Site is not using HTTPS")
                        security_data["score"] -= 30
                    
                    # Check security headers
                    headers = response.headers
                    security_headers = {
                        'X-Frame-Options': 'Prevents clickjacking attacks',
                        'X-Content-Type-Options': 'Prevents MIME type sniffing',
                        'X-XSS-Protection': 'Enables XSS filtering',
                        'Strict-Transport-Security': 'Enforces HTTPS',
                        'Content-Security-Policy': 'Prevents XSS attacks'
                    }
                    
                    for header, description in security_headers.items():
                        if header not in headers:
                            security_data["issues"].append(f"Missing security header: {header}")
                            security_data["score"] -= 10
                    
                    # Check for mixed content
                    content = await response.text()
                    if 'http://' in content and url.startswith('https://'):
                        security_data["issues"].append("Mixed content detected (HTTP resources on HTTPS page)")
                        security_data["score"] -= 15
                    
                    security_data["total_issues"] = len(security_data["issues"])
                    security_data["recommendations"] = self._get_security_recommendations(security_data["issues"])
                    
                    return security_data
                    
        except Exception as e:
            return {"error": str(e), "score": 0}
    
    async def analyze_content(self, url: str) -> Dict[str, Any]:
        """Analyze content quality and structure"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=30) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    # Get text content
                    text = soup.get_text()
                    words = text.split()
                    
                    content_data = {
                        "word_count": len(words),
                        "score": 100,
                        "issues": [],
                        "recommendations": []
                    }
                    
                    # Check content length
                    if len(words) < 300:
                        content_data["issues"].append("Content is too short (less than 300 words)")
                        content_data["score"] -= 20
                    elif len(words) > 2000:
                        content_data["issues"].append("Content is very long (more than 2000 words)")
                        content_data["score"] -= 5
                    
                    # Check for headings structure
                    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
                    if len(headings) < 2:
                        content_data["issues"].append("Insufficient heading structure")
                        content_data["score"] -= 10
                    
                    # Check for paragraphs
                    paragraphs = soup.find_all('p')
                    if len(paragraphs) < 3:
                        content_data["issues"].append("Insufficient paragraph structure")
                        content_data["score"] -= 10
                    
                    # Check for lists
                    lists = soup.find_all(['ul', 'ol'])
                    if len(lists) == 0 and len(words) > 500:
                        content_data["issues"].append("Long content without lists for better readability")
                        content_data["score"] -= 5
                    
                    content_data["total_issues"] = len(content_data["issues"])
                    content_data["recommendations"] = self._get_content_recommendations(content_data["issues"])
                    
                    return content_data
                    
        except Exception as e:
            return {"error": str(e), "score": 0}
    
    def _calculate_performance_score(self, load_time: float, content_size: int, status_code: int) -> int:
        """Calculate performance score based on metrics"""
        score = 100
        
        # Load time scoring
        if load_time > 3:
            score -= 30
        elif load_time > 2:
            score -= 20
        elif load_time > 1:
            score -= 10
        
        # Content size scoring
        if content_size > 1000000:  # > 1MB
            score -= 20
        elif content_size > 500000:  # > 500KB
            score -= 10
        
        # Status code
        if status_code != 200:
            score -= 20
        
        return max(0, score)
    
    def _get_performance_recommendations(self, load_time: float, content_size: int, unoptimized_images: int) -> List[str]:
        """Get performance improvement recommendations"""
        recommendations = []
        
        if load_time > 2:
            recommendations.append("Optimize page load time - consider using a CDN or optimizing server response")
        
        if content_size > 500000:
            recommendations.append("Reduce page size by minifying CSS, JavaScript, and HTML")
        
        if unoptimized_images > 0:
            recommendations.append(f"Optimize {unoptimized_images} large images - compress and use modern formats like WebP")
        
        return recommendations
    
    def _get_accessibility_recommendations(self, issues: List[str]) -> List[str]:
        """Get accessibility improvement recommendations"""
        recommendations = []
        
        if any("alt text" in issue for issue in issues):
            recommendations.append("Add descriptive alt text to all images")
        
        if any("H1" in issue for issue in issues):
            recommendations.append("Ensure proper heading hierarchy with one H1 per page")
        
        if any("labels" in issue for issue in issues):
            recommendations.append("Add proper labels to all form inputs")
        
        if any("color contrast" in issue for issue in issues):
            recommendations.append("Test and improve color contrast ratios")
        
        return recommendations
    
    def _get_seo_recommendations(self, issues: List[str]) -> List[str]:
        """Get SEO improvement recommendations"""
        recommendations = []
        
        if any("title" in issue for issue in issues):
            recommendations.append("Optimize title tag - keep it between 30-60 characters")
        
        if any("meta description" in issue for issue in issues):
            recommendations.append("Add and optimize meta description - keep it between 120-160 characters")
        
        if any("H1" in issue for issue in issues):
            recommendations.append("Use proper heading structure with one H1 per page")
        
        if any("alt text" in issue for issue in issues):
            recommendations.append("Add descriptive alt text to images for better SEO")
        
        if any("structured data" in issue for issue in issues):
            recommendations.append("Implement structured data (JSON-LD) for better search visibility")
        
        return recommendations
    
    def _get_security_recommendations(self, issues: List[str]) -> List[str]:
        """Get security improvement recommendations"""
        recommendations = []
        
        if any("HTTPS" in issue for issue in issues):
            recommendations.append("Implement HTTPS with SSL certificate")
        
        if any("security header" in issue for issue in issues):
            recommendations.append("Add missing security headers to protect against common attacks")
        
        if any("mixed content" in issue for issue in issues):
            recommendations.append("Fix mixed content issues by using HTTPS for all resources")
        
        return recommendations
    
    def _get_content_recommendations(self, issues: List[str]) -> List[str]:
        """Get content improvement recommendations"""
        recommendations = []
        
        if any("too short" in issue for issue in issues):
            recommendations.append("Add more valuable content to improve user engagement")
        
        if any("heading structure" in issue for issue in issues):
            recommendations.append("Improve content structure with proper headings")
        
        if any("paragraph" in issue for issue in issues):
            recommendations.append("Break content into more paragraphs for better readability")
        
        if any("lists" in issue for issue in issues):
            recommendations.append("Use lists and bullet points to improve content readability")
        
        return recommendations
