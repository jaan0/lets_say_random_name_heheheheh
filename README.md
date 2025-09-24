# AI-Powered Website Analyzer

A comprehensive website analysis tool that provides detailed insights into website performance, accessibility, SEO, security, and content quality. Built with Python FastAPI backend and Next.js frontend, designed for easy deployment on Vercel.

## 🚀 Features

- **One-Click Analysis**: Simply enter a URL and get comprehensive website insights
- **Performance Testing**: Load time, page size, image optimization analysis
- **Accessibility Audit**: WCAG compliance, alt text, heading structure checks
- **SEO Analysis**: Meta tags, content structure, internal linking analysis
- **Security Assessment**: HTTPS, security headers, mixed content detection
- **Content Quality**: Word count, structure, readability analysis
- **AI-Powered Insights**: Smart recommendations and scoring
- **Professional PDF Reports**: Downloadable, well-documented analysis reports
- **Real-time Progress**: Live updates during analysis
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **aiohttp**: Async HTTP client for website analysis
- **BeautifulSoup**: HTML parsing and content analysis
- **ReportLab**: PDF report generation
- **Pydantic**: Data validation and serialization

### Frontend
- **Next.js**: React framework with SSR
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Lucide React**: Beautiful icons
- **React Hot Toast**: Toast notifications

### Deployment
- **Vercel**: Serverless deployment platform
- **Serverless Functions**: Scalable backend architecture

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.8+
- Vercel account (for deployment)

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd website-analyzer
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   npm install
   ```

4. **Run the development server**
   ```bash
   # Terminal 1: Start the Python backend
   cd api
   uvicorn main:app --reload --port 8000
   
   # Terminal 2: Start the Next.js frontend
   npm run dev
   ```

5. **Open your browser**
   Navigate to `http://localhost:3000`

### Vercel Deployment

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Deploy to Vercel**
   ```bash
   vercel
   ```

3. **Configure environment variables** (if needed)
   ```bash
   vercel env add VARIABLE_NAME
   ```

## 📁 Project Structure

```
website-analyzer/
├── api/                          # Backend API
│   ├── main.py                   # Main FastAPI application
│   ├── analyzer.py               # Website analysis logic
│   ├── report_generator.py       # PDF report generation
│   ├── analyze.py                # Analysis endpoint
│   ├── analysis/                 # Analysis status endpoints
│   └── download/                 # Report download endpoints
├── pages/                        # Next.js pages
│   ├── index.tsx                 # Main application page
│   └── _app.tsx                  # App configuration
├── styles/                       # CSS styles
│   └── globals.css               # Global styles
├── reports/                      # Generated PDF reports
├── package.json                  # Node.js dependencies
├── requirements.txt              # Python dependencies
├── vercel.json                   # Vercel configuration
├── tailwind.config.js            # Tailwind CSS config
├── next.config.js                # Next.js configuration
└── README.md                     # This file
```

## 🔧 API Endpoints

### POST `/api/analyze`
Start website analysis
```json
{
  "url": "https://example.com",
  "options": {}
}
```

### GET `/api/analysis/{analysis_id}`
Get analysis status and results

### GET `/api/download/{analysis_id}`
Download PDF report

## 📊 Analysis Categories

### Performance (⚡)
- Page load time
- Total page size
- Image optimization
- HTTP status codes
- Server response time

### Accessibility (♿)
- Alt text for images
- Heading structure
- Form labels
- Color contrast
- Keyboard navigation

### SEO (🔍)
- Title tags
- Meta descriptions
- Heading hierarchy
- Internal linking
- Structured data
- Image alt attributes

### Security (🔒)
- HTTPS implementation
- Security headers
- Mixed content detection
- XSS protection
- Content Security Policy

### Content Quality (📝)
- Word count
- Content structure
- Readability
- Heading organization
- Paragraph structure

## 🎯 Usage

1. **Enter URL**: Input the website URL you want to analyze
2. **Start Analysis**: Click the "Start Analysis" button
3. **Monitor Progress**: Watch real-time progress updates
4. **View Results**: See detailed scores and recommendations
5. **Download Report**: Get a comprehensive PDF report

## 📈 Scoring System

- **90-100**: Excellent
- **80-89**: Good
- **70-79**: Fair
- **60-69**: Poor
- **0-59**: Critical

## 🔒 Security Features

- CORS protection
- Input validation
- Error handling
- Rate limiting (recommended for production)
- Secure PDF generation

## 🚀 Performance Optimizations

- Async/await for non-blocking operations
- Efficient HTML parsing
- Optimized image analysis
- Cached results (in-memory)
- Serverless architecture for scalability

## 🛠️ Customization

### Adding New Analysis Categories
1. Extend the `WebsiteAnalyzer` class
2. Add new analysis methods
3. Update the PDF report generator
4. Modify the frontend to display results

### Customizing PDF Reports
1. Edit `report_generator.py`
2. Modify styles and layout
3. Add new sections or metrics
4. Customize branding and colors

## 📝 Environment Variables

```bash
# Optional: Add these to your Vercel environment
ANALYSIS_TIMEOUT=300
MAX_CONCURRENT_ANALYSES=10
REPORT_RETENTION_DAYS=7
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the API endpoints

## 🔮 Future Enhancements

- [ ] Lighthouse integration for advanced performance metrics
- [ ] Mobile responsiveness testing
- [ ] Multi-page analysis
- [ ] Historical analysis tracking
- [ ] Team collaboration features
- [ ] API rate limiting
- [ ] Database integration for result persistence
- [ ] Advanced security scanning
- [ ] Content quality AI analysis
- [ ] Competitive analysis features

---

Built with ❤️ for the web development community
