CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ip_address INET UNIQUE NOT NULL,
    user_agent TEXT,
    browser VARCHAR(50),
    operating_system VARCHAR(50),
    is_mobile BOOLEAN DEFAULT FALSE,
    country VARCHAR(100),
    city VARCHAR(100),
    name VARCHAR(255),
    email VARCHAR(255),
    contact VARCHAR(255),
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS analyses (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    ip_address INET,
    user_agent TEXT,
    browser VARCHAR(50),
    operating_system VARCHAR(50),
    is_mobile BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) DEFAULT 'started',
    results JSONB,
    overall_score INTEGER,
    pdf_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS analytics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    date DATE DEFAULT CURRENT_DATE,
    total_analyses INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    avg_score DECIMAL(5,2),
    top_countries JSONB,
    browser_stats JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX IF NOT EXISTS idx_users_ip_address ON users(ip_address);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);
CREATE INDEX IF NOT EXISTS idx_analyses_user_id ON analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at);
CREATE INDEX IF NOT EXISTS idx_analyses_status ON analyses(status);
CREATE INDEX IF NOT EXISTS idx_analyses_url ON analyses(url);
CREATE INDEX IF NOT EXISTS idx_analytics_date ON analytics(date);


CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE analytics ENABLE ROW LEVEL SECURITY;


CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (ip_address = inet_client_addr());

CREATE POLICY "Users can insert own data" ON users
    FOR INSERT WITH CHECK (ip_address = inet_client_addr());

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (ip_address = inet_client_addr());


CREATE POLICY "Users can view own analyses" ON analyses
    FOR SELECT USING (ip_address = inet_client_addr());

CREATE POLICY "Users can insert own analyses" ON analyses
    FOR INSERT WITH CHECK (ip_address = inet_client_addr());

CREATE POLICY "Users can update own analyses" ON analyses
    FOR UPDATE USING (ip_address = inet_client_addr());

CREATE POLICY "Analytics are viewable by authenticated users" ON analytics
    FOR SELECT USING (true);

CREATE OR REPLACE FUNCTION get_user_analytics(user_ip INET)
RETURNS TABLE (
    total_analyses BIGINT,
    avg_score DECIMAL,
    last_analysis_date TIMESTAMP WITH TIME ZONE,
    favorite_browser VARCHAR,
    most_analyzed_domain TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(a.id) as total_analyses,
        AVG(a.overall_score) as avg_score,
        MAX(a.created_at) as last_analysis_date,
        MODE() WITHIN GROUP (ORDER BY a.browser) as favorite_browser,
        MODE() WITHIN GROUP (ORDER BY split_part(a.url, '/', 3)) as most_analyzed_domain
    FROM analyses a
    WHERE a.ip_address = user_ip;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE OR REPLACE FUNCTION get_global_analytics()
RETURNS TABLE (
    total_analyses BIGINT,
    unique_users BIGINT,
    avg_score DECIMAL,
    top_countries JSONB,
    browser_stats JSONB,
    daily_analyses JSONB
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(a.id) as total_analyses,
        COUNT(DISTINCT a.ip_address) as unique_users,
        AVG(a.overall_score) as avg_score,
        jsonb_object_agg(country, country_count) as top_countries,
        jsonb_object_agg(browser, browser_count) as browser_stats,
        jsonb_object_agg(analysis_date, daily_count) as daily_analyses
    FROM (
        SELECT 
            u.country,
            COUNT(*) as country_count
        FROM users u
        GROUP BY u.country
    ) country_stats,
    (
        SELECT 
            a.browser,
            COUNT(*) as browser_count
        FROM analyses a
        GROUP BY a.browser
    ) browser_stats,
    (
        SELECT 
            DATE(a.created_at) as analysis_date,
            COUNT(*) as daily_count
        FROM analyses a
        WHERE a.created_at >= NOW() - INTERVAL '30 days'
        GROUP BY DATE(a.created_at)
    ) daily_stats;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

INSERT INTO users (ip_address, browser, operating_system, country, city) 
VALUES 
    ('127.0.0.1', 'Chrome', 'Windows', 'US', 'New York'),
    ('192.168.1.1', 'Firefox', 'macOS', 'CA', 'Toronto')
ON CONFLICT (ip_address) DO NOTHING;

GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
