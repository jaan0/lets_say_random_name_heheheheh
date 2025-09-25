# Supabase Database Setup Guide

## 1. Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Note down your project URL and anon key

## 2. Set Environment Variables

Create a `.env.local` file in your project root with:

```env
NEXT_PUBLIC_SUPABASE_URL=your-supabase-project-url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-supabase-anon-key
```

## 3. Run Database Schema

1. Go to your Supabase dashboard
2. Navigate to SQL Editor
3. Copy and paste the contents of `supabase-schema.sql`
4. Run the SQL to create tables and functions

## 4. Database Tables Created

### Users Table
- Stores user information (IP, browser, location, contact info)
- Tracks user preferences and last seen

### Analyses Table
- Stores all website analysis results
- Links to users via foreign key
- Contains analysis data, scores, and PDF paths

### Analytics Table
- Aggregated analytics data
- Daily statistics and trends

## 5. Features Enabled

- **User Tracking**: IP, browser, OS, location detection
- **Analysis Storage**: All results saved to database
- **PDF Reports**: Downloadable links stored in DB
- **Analytics**: User behavior and analysis trends
- **Privacy**: Cookie consent and user preferences

## 6. Data You'll Have Access To

- User IP addresses and locations
- Browser and device information
- All analyzed websites and their URLs
- Analysis results and scores
- PDF report download links
- User contact information (if provided)
- Analysis timestamps and frequency

## 7. Privacy & Compliance

- Cookie consent system implemented
- User can opt-out of analytics
- GDPR-compliant data handling
- Row-level security enabled
- User data can be deleted on request
