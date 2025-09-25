import { createClient } from '@supabase/supabase-js';

// Supabase configuration
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'your-supabase-url';
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'your-supabase-anon-key';

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseKey);

// Database operations
export class SupabaseDB {
  constructor() {
    this.client = supabase;
  }

  // Save user analysis to database
  async saveAnalysis(data) {
    try {
      const { data: result, error } = await this.client
        .from('analyses')
        .insert([data])
        .select()
        .single();

      if (error) {
        console.error('Error saving analysis:', error);
        throw error;
      }

      return result;
    } catch (error) {
      console.error('Database error:', error);
      throw error;
    }
  }

  // Get analysis by ID
  async getAnalysis(analysisId) {
    try {
      const { data, error } = await this.client
        .from('analyses')
        .select('*')
        .eq('id', analysisId)
        .single();

      if (error) {
        console.error('Error fetching analysis:', error);
        return null;
      }

      return data;
    } catch (error) {
      console.error('Database error:', error);
      return null;
    }
  }

  // Get all analyses for a user
  async getUserAnalyses(userId) {
    try {
      const { data, error } = await this.client
        .from('analyses')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching user analyses:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Database error:', error);
      return [];
    }
  }

  // Save or update user information
  async saveUser(userData) {
    try {
      const { data, error } = await this.client
        .from('users')
        .upsert([userData], { onConflict: 'ip_address' })
        .select()
        .single();

      if (error) {
        console.error('Error saving user:', error);
        throw error;
      }

      return data;
    } catch (error) {
      console.error('Database error:', error);
      throw error;
    }
  }

  // Get user by IP
  async getUserByIP(ipAddress) {
    try {
      const { data, error } = await this.client
        .from('users')
        .select('*')
        .eq('ip_address', ipAddress)
        .single();

      if (error && error.code !== 'PGRST116') { // PGRST116 = no rows returned
        console.error('Error fetching user:', error);
        return null;
      }

      return data;
    } catch (error) {
      console.error('Database error:', error);
      return null;
    }
  }

  // Get analytics data
  async getAnalytics() {
    try {
      const { data, error } = await this.client
        .from('analyses')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(100);

      if (error) {
        console.error('Error fetching analytics:', error);
        return [];
      }

      return data || [];
    } catch (error) {
      console.error('Database error:', error);
      return [];
    }
  }
}

export default SupabaseDB;
