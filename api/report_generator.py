import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime
from typing import Dict, Any
import asyncio

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
        # Create reports directory if it doesn't exist
        os.makedirs("reports", exist_ok=True)
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue
        ))
        
        # Score style
        self.styles.add(ParagraphStyle(
            name='Score',
            parent=self.styles['Normal'],
            fontSize=14,
            alignment=TA_CENTER,
            textColor=colors.darkgreen
        ))
        
        # Issue style
        self.styles.add(ParagraphStyle(
            name='Issue',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            textColor=colors.red
        ))
        
        # Recommendation style
        self.styles.add(ParagraphStyle(
            name='Recommendation',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            textColor=colors.blue
        ))
    
    async def generate_report(self, analysis_data: Dict[str, Any], analysis_id: str) -> str:
        """Generate comprehensive PDF report"""
        filename = f"reports/{analysis_id}.pdf"
        doc = SimpleDocTemplate(filename, pagesize=A4)
        story = []
        
        # Title page
        story.append(Paragraph("Website Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Basic info
        story.append(Paragraph(f"<b>Website URL:</b> {analysis_data['url']}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Analysis Date:</b> {analysis_data['analyzed_at']}", self.styles['Normal']))
        story.append(Paragraph(f"<b>Overall Score:</b> {analysis_data['overall_score']}/100", self.styles['Score']))
        story.append(Spacer(1, 30))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        summary = self._generate_executive_summary(analysis_data)
        story.append(Paragraph(summary, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Performance Analysis
        if 'performance' in analysis_data and analysis_data['performance']:
            story.append(Paragraph("Performance Analysis", self.styles['SectionHeader']))
            story.extend(self._generate_performance_section(analysis_data['performance']))
            story.append(Spacer(1, 20))
        
        # Accessibility Analysis
        if 'accessibility' in analysis_data and analysis_data['accessibility']:
            story.append(Paragraph("Accessibility Analysis", self.styles['SectionHeader']))
            story.extend(self._generate_accessibility_section(analysis_data['accessibility']))
            story.append(Spacer(1, 20))
        
        # SEO Analysis
        if 'seo' in analysis_data and analysis_data['seo']:
            story.append(Paragraph("SEO Analysis", self.styles['SectionHeader']))
            story.extend(self._generate_seo_section(analysis_data['seo']))
            story.append(Spacer(1, 20))
        
        # Security Analysis
        if 'security' in analysis_data and analysis_data['security']:
            story.append(Paragraph("Security Analysis", self.styles['SectionHeader']))
            story.extend(self._generate_security_section(analysis_data['security']))
            story.append(Spacer(1, 20))
        
        # Content Analysis
        if 'content' in analysis_data and analysis_data['content']:
            story.append(Paragraph("Content Analysis", self.styles['SectionHeader']))
            story.extend(self._generate_content_section(analysis_data['content']))
            story.append(Spacer(1, 20))
        
        # Recommendations Summary
        story.append(Paragraph("Priority Recommendations", self.styles['SectionHeader']))
        recommendations = self._generate_priority_recommendations(analysis_data)
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        # Build PDF
        doc.build(story)
        return filename
    
    def _generate_executive_summary(self, analysis_data: Dict[str, Any]) -> str:
        """Generate executive summary"""
        overall_score = analysis_data.get('overall_score', 0)
        
        if overall_score >= 90:
            grade = "Excellent"
            color = "green"
        elif overall_score >= 80:
            grade = "Good"
            color = "blue"
        elif overall_score >= 70:
            grade = "Fair"
            color = "orange"
        elif overall_score >= 60:
            grade = "Poor"
            color = "red"
        else:
            grade = "Critical"
            color = "darkred"
        
        summary = f"""
        This website analysis reveals an overall score of {overall_score}/100, which is rated as <b>{grade}</b>.
        
        The analysis covers five key areas: Performance, Accessibility, SEO, Security, and Content Quality.
        Each area has been evaluated based on industry best practices and current web standards.
        
        """
        
        # Add specific highlights
        highlights = []
        for category in ['performance', 'accessibility', 'seo', 'security', 'content']:
            if category in analysis_data and analysis_data[category]:
                score = analysis_data[category].get('score', 0)
                if score >= 90:
                    highlights.append(f"{category.title()}: Excellent")
                elif score >= 70:
                    highlights.append(f"{category.title()}: Good")
                else:
                    highlights.append(f"{category.title()}: Needs Improvement")
        
        if highlights:
            summary += f"<b>Key Findings:</b><br/>" + "<br/>".join(highlights)
        
        return summary
    
    def _generate_performance_section(self, performance_data: Dict[str, Any]) -> list:
        """Generate performance analysis section"""
        elements = []
        
        score = performance_data.get('score', 0)
        elements.append(Paragraph(f"<b>Performance Score: {score}/100</b>", self.styles['Score']))
        elements.append(Spacer(1, 10))
        
        # Metrics table
        metrics_data = [
            ['Metric', 'Value', 'Status'],
            ['Load Time', f"{performance_data.get('load_time', 0)}s", self._get_status_indicator(performance_data.get('load_time', 0), 2, 's')],
            ['Page Size', f"{performance_data.get('page_size', 0):,} bytes", self._get_status_indicator(performance_data.get('page_size', 0), 500000, 'bytes')],
            ['Status Code', str(performance_data.get('status_code', 0)), self._get_status_indicator(performance_data.get('status_code', 0), 200, 'code')],
            ['Total Images', str(performance_data.get('total_images', 0)), 'Info'],
            ['Unoptimized Images', str(performance_data.get('unoptimized_images', 0)), self._get_status_indicator(performance_data.get('unoptimized_images', 0), 0, 'count', reverse=True)]
        ]
        
        table = Table(metrics_data, colWidths=[2*inch, 1.5*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 10))
        
        # Recommendations
        recommendations = performance_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Recommendations:</b>", self.styles['Normal']))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        return elements
    
    def _generate_accessibility_section(self, accessibility_data: Dict[str, Any]) -> list:
        """Generate accessibility analysis section"""
        elements = []
        
        score = accessibility_data.get('score', 0)
        elements.append(Paragraph(f"<b>Accessibility Score: {score}/100</b>", self.styles['Score']))
        elements.append(Spacer(1, 10))
        
        # Issues
        issues = accessibility_data.get('issues', [])
        if issues:
            elements.append(Paragraph("<b>Issues Found:</b>", self.styles['Normal']))
            for issue in issues:
                elements.append(Paragraph(f"• {issue}", self.styles['Issue']))
            elements.append(Spacer(1, 10))
        
        # Recommendations
        recommendations = accessibility_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Recommendations:</b>", self.styles['Normal']))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        return elements
    
    def _generate_seo_section(self, seo_data: Dict[str, Any]) -> list:
        """Generate SEO analysis section"""
        elements = []
        
        score = seo_data.get('score', 0)
        elements.append(Paragraph(f"<b>SEO Score: {score}/100</b>", self.styles['Score']))
        elements.append(Spacer(1, 10))
        
        # Issues
        issues = seo_data.get('issues', [])
        if issues:
            elements.append(Paragraph("<b>Issues Found:</b>", self.styles['Normal']))
            for issue in issues:
                elements.append(Paragraph(f"• {issue}", self.styles['Issue']))
            elements.append(Spacer(1, 10))
        
        # Recommendations
        recommendations = seo_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Recommendations:</b>", self.styles['Normal']))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        return elements
    
    def _generate_security_section(self, security_data: Dict[str, Any]) -> list:
        """Generate security analysis section"""
        elements = []
        
        score = security_data.get('score', 0)
        elements.append(Paragraph(f"<b>Security Score: {score}/100</b>", self.styles['Score']))
        elements.append(Spacer(1, 10))
        
        # Issues
        issues = security_data.get('issues', [])
        if issues:
            elements.append(Paragraph("<b>Security Issues:</b>", self.styles['Normal']))
            for issue in issues:
                elements.append(Paragraph(f"• {issue}", self.styles['Issue']))
            elements.append(Spacer(1, 10))
        
        # Recommendations
        recommendations = security_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Security Recommendations:</b>", self.styles['Normal']))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        return elements
    
    def _generate_content_section(self, content_data: Dict[str, Any]) -> list:
        """Generate content analysis section"""
        elements = []
        
        score = content_data.get('score', 0)
        elements.append(Paragraph(f"<b>Content Score: {score}/100</b>", self.styles['Score']))
        elements.append(Spacer(1, 10))
        
        # Content metrics
        word_count = content_data.get('word_count', 0)
        elements.append(Paragraph(f"<b>Word Count:</b> {word_count:,} words", self.styles['Normal']))
        elements.append(Spacer(1, 10))
        
        # Issues
        issues = content_data.get('issues', [])
        if issues:
            elements.append(Paragraph("<b>Content Issues:</b>", self.styles['Normal']))
            for issue in issues:
                elements.append(Paragraph(f"• {issue}", self.styles['Issue']))
            elements.append(Spacer(1, 10))
        
        # Recommendations
        recommendations = content_data.get('recommendations', [])
        if recommendations:
            elements.append(Paragraph("<b>Content Recommendations:</b>", self.styles['Normal']))
            for rec in recommendations:
                elements.append(Paragraph(f"• {rec}", self.styles['Recommendation']))
        
        return elements
    
    def _generate_priority_recommendations(self, analysis_data: Dict[str, Any]) -> list:
        """Generate priority recommendations based on all analysis data"""
        all_recommendations = []
        
        # Collect all recommendations
        for category in ['performance', 'accessibility', 'seo', 'security', 'content']:
            if category in analysis_data and analysis_data[category]:
                category_data = analysis_data[category]
                score = category_data.get('score', 0)
                recommendations = category_data.get('recommendations', [])
                
                # Prioritize recommendations based on score
                if score < 70:  # Low scores get higher priority
                    for rec in recommendations:
                        all_recommendations.append(f"[{category.upper()}] {rec}")
        
        # Return top 10 recommendations
        return all_recommendations[:10]
    
    def _get_status_indicator(self, value: float, threshold: float, unit: str, reverse: bool = False) -> str:
        """Get status indicator for metrics"""
        if unit == 's':  # seconds
            if value <= threshold:
                return "Good"
            elif value <= threshold * 1.5:
                return "Fair"
            else:
                return "Poor"
        elif unit == 'bytes':
            if value <= threshold:
                return "Good"
            elif value <= threshold * 2:
                return "Fair"
            else:
                return "Poor"
        elif unit == 'code':
            if value == 200:
                return "Good"
            else:
                return "Poor"
        elif unit == 'count':
            if reverse:
                if value == 0:
                    return "Good"
                elif value <= 3:
                    return "Fair"
                else:
                    return "Poor"
            else:
                if value <= threshold:
                    return "Good"
                elif value <= threshold * 2:
                    return "Fair"
                else:
                    return "Poor"
        else:
            return "Info"
