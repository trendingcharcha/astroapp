-- ============================================================
-- KarmaQuest Supabase Database Setup Script
-- Run this in your Supabase SQL Editor to create the tables
-- ============================================================

-- 1. Enable UUID extension (usually already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 2. karma_profiles table
-- Stores each user's onboarding profile, goal, XP
CREATE TABLE IF NOT EXISTS karma_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  name TEXT,
  gender TEXT DEFAULT 'M',
  dob TEXT,
  tob TEXT,
  pob TEXT,
  onboarding_path TEXT DEFAULT 'single',
  goal TEXT DEFAULT 'job',
  profession TEXT,
  custom_issue TEXT,
  property_number TEXT,
  property_type TEXT,
  property_city TEXT,
  baby_number TEXT,
  first_baby_dob TEXT,
  first_baby_age TEXT,
  second_baby_age TEXT,
  include_partner BOOLEAN DEFAULT false,
  partner_name TEXT,
  partner_dob TEXT,
  partner_tob TEXT,
  partner_pob TEXT,
  partner_gender TEXT DEFAULT 'F',
  total_xp INTEGER DEFAULT 0,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE karma_profiles ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read/write their own profile
CREATE POLICY "Users can manage their own profile"
  ON karma_profiles
  FOR ALL
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- 3. karma_tasks table
-- Stores daily quest tasks for each user
CREATE TABLE IF NOT EXISTS karma_tasks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  description TEXT,
  xp INTEGER DEFAULT 10,
  is_completed BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE karma_tasks ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only read/write their own tasks
CREATE POLICY "Users can manage their own tasks"
  ON karma_tasks
  FOR ALL
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- 4. Optional: Enable anonymous sign-in in Supabase Dashboard
-- Go to: Authentication → Providers → Anonymous → Enable
-- This allows Guest Mode logins without an email/password.

-- ============================================================
-- DONE! Your KarmaQuest database is ready.
-- ============================================================
