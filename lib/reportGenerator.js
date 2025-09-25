import jsPDF from 'jspdf';
import fs from 'fs';

class PDFReportGenerator {
  constructor() {
    this.doc = new jsPDF();
  }

  generateReport(analysisData, analysisId) {
    try {
      const doc = new jsPDF();
      
      // Title
      doc.setFontSize(20);
      doc.text('Website Analysis Report', 20, 30);
      
      // Analysis info
      doc.setFontSize(12);
      doc.text(`Analysis ID: ${analysisId}`, 20, 50);
      doc.text(`URL: ${analysisData.url}`, 20, 60);
      doc.text(`Analyzed: ${analysisData.analyzed_at}`, 20, 70);
      
      // Overall Score
      doc.setFontSize(16);
      doc.text(`Overall Score: ${analysisData.overall_score}/100`, 20, 90);
      
      let yPosition = 110;
      
      // Performance Section
      if (analysisData.performance) {
        doc.setFontSize(14);
        doc.text('Performance Analysis', 20, yPosition);
        yPosition += 10;
        
        doc.setFontSize(10);
        doc.text(`Score: ${analysisData.performance.score}/100`, 20, yPosition);
        yPosition += 8;
        doc.text(`Load Time: ${analysisData.performance.load_time}ms`, 20, yPosition);
        yPosition += 8;
        doc.text(`Page Size: ${analysisData.performance.page_size} bytes`, 20, yPosition);
        yPosition += 8;
        doc.text(`Status Code: ${analysisData.performance.status_code}`, 20, yPosition);
        yPosition += 15;
      }
      
      // Accessibility Section
      if (analysisData.accessibility) {
        doc.setFontSize(14);
        doc.text('Accessibility Analysis', 20, yPosition);
        yPosition += 10;
        
        doc.setFontSize(10);
        doc.text(`Score: ${analysisData.accessibility.score}/100`, 20, yPosition);
        yPosition += 8;
        doc.text(`Issues Found: ${analysisData.accessibility.total_issues}`, 20, yPosition);
        yPosition += 8;
        
        if (analysisData.accessibility.issues && analysisData.accessibility.issues.length > 0) {
          doc.text('Issues:', 20, yPosition);
          yPosition += 8;
          analysisData.accessibility.issues.forEach(issue => {
            doc.text(`• ${issue}`, 25, yPosition);
            yPosition += 6;
          });
        }
        yPosition += 10;
      }
      
      // SEO Section
      if (analysisData.seo) {
        doc.setFontSize(14);
        doc.text('SEO Analysis', 20, yPosition);
        yPosition += 10;
        
        doc.setFontSize(10);
        doc.text(`Score: ${analysisData.seo.score}/100`, 20, yPosition);
        yPosition += 8;
        doc.text(`Issues Found: ${analysisData.seo.total_issues}`, 20, yPosition);
        yPosition += 8;
        
        if (analysisData.seo.issues && analysisData.seo.issues.length > 0) {
          doc.text('Issues:', 20, yPosition);
          yPosition += 8;
          analysisData.seo.issues.forEach(issue => {
            doc.text(`• ${issue}`, 25, yPosition);
            yPosition += 6;
          });
        }
        yPosition += 10;
      }
      
      // Security Section
      if (analysisData.security) {
        doc.setFontSize(14);
        doc.text('Security Analysis', 20, yPosition);
        yPosition += 10;
        
        doc.setFontSize(10);
        doc.text(`Score: ${analysisData.security.score}/100`, 20, yPosition);
        yPosition += 8;
        doc.text(`Issues Found: ${analysisData.security.total_issues}`, 20, yPosition);
        yPosition += 8;
        
        if (analysisData.security.issues && analysisData.security.issues.length > 0) {
          doc.text('Issues:', 20, yPosition);
          yPosition += 8;
          analysisData.security.issues.forEach(issue => {
            doc.text(`• ${issue}`, 25, yPosition);
            yPosition += 6;
          });
        }
        yPosition += 10;
      }
      
      // Content Section
      if (analysisData.content) {
        doc.setFontSize(14);
        doc.text('Content Analysis', 20, yPosition);
        yPosition += 10;
        
        doc.setFontSize(10);
        doc.text(`Score: ${analysisData.content.score}/100`, 20, yPosition);
        yPosition += 8;
        doc.text(`Word Count: ${analysisData.content.word_count}`, 20, yPosition);
        yPosition += 8;
        doc.text(`Headings: ${analysisData.content.heading_count}`, 20, yPosition);
        yPosition += 8;
        doc.text(`Paragraphs: ${analysisData.content.paragraph_count}`, 20, yPosition);
        yPosition += 8;
        doc.text(`Links: ${analysisData.content.link_count}`, 20, yPosition);
        yPosition += 8;
        doc.text(`Images: ${analysisData.content.image_count}`, 20, yPosition);
      }
      
      // Save the PDF
      const pdfPath = `/tmp/reports/${analysisId}.pdf`;
      const reportsDir = '/tmp/reports';
      
      if (!fs.existsSync(reportsDir)) {
        fs.mkdirSync(reportsDir, { recursive: true });
      }
      
      doc.save(pdfPath);
      return pdfPath;
      
    } catch (error) {
      console.error('Error generating PDF report:', error);
      throw error;
    }
  }
}

export default PDFReportGenerator;
