-- ============================================================================
-- COSMOVEDIC & KARMAQUEST SECURE SUPABASE BACKEND (SINGLE BAAS CONFIGURATION)
-- IMPENETRABLE ROW-LEVEL SECURITY (RLS), JWT AUTH & ANTI-SCRAPING POLICIES
-- ============================================================================

-- 1. CREATE USER PROFILES TABLE (LOCKED DOWN BY RLS)
CREATE TABLE IF NOT EXISTS public.profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name TEXT NOT NULL,
  gender TEXT NOT NULL CHECK (gender IN ('M', 'F')),
  dob DATE NOT NULL,
  tob TIME NOT NULL,
  pob TEXT NOT NULL,
  lat DOUBLE PRECISION NOT NULL,
  lng DOUBLE PRECISION NOT NULL,
  timezone DOUBLE PRECISION NOT NULL DEFAULT 5.5,
  active_goals JSONB NOT NULL DEFAULT '["job"]'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. CREATE 90-DAY KARMIC PROGRESS TRAIL TABLE (LOCKED DOWN BY RLS)
CREATE TABLE IF NOT EXISTS public.karmic_progress (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  roadmap_day INT NOT NULL CHECK (roadmap_day BETWEEN 1 AND 90),
  task_states JSONB NOT NULL DEFAULT '[false, false, false, false]'::jsonb,
  xp_gained INT NOT NULL DEFAULT 0,
  completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE (user_id, roadmap_day)
);

-- 3. ENABLE ROW LEVEL SECURITY (RLS) ON ALL TABLES
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.karmic_progress ENABLE ROW LEVEL SECURITY;

-- 4. STRICT IDEMPOTENT RLS POLICIES FOR PROFILES
DROP POLICY IF EXISTS "Profiles: User read own profile" ON public.profiles;
CREATE POLICY "Profiles: User read own profile"
  ON public.profiles FOR SELECT
  USING (auth.uid() = id);

DROP POLICY IF EXISTS "Profiles: User update own profile" ON public.profiles;
CREATE POLICY "Profiles: User update own profile"
  ON public.profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

DROP POLICY IF EXISTS "Profiles: User insert own profile" ON public.profiles;
CREATE POLICY "Profiles: User insert own profile"
  ON public.profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- 5. STRICT IDEMPOTENT RLS POLICIES FOR KARMIC PROGRESS
DROP POLICY IF EXISTS "Progress: User read own progress" ON public.karmic_progress;
CREATE POLICY "Progress: User read own progress"
  ON public.karmic_progress FOR SELECT
  USING (auth.uid() = user_id);

DROP POLICY IF EXISTS "Progress: User update own progress" ON public.karmic_progress;
CREATE POLICY "Progress: User update own progress"
  ON public.karmic_progress FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

DROP POLICY IF EXISTS "Progress: User insert own progress" ON public.karmic_progress;
CREATE POLICY "Progress: User insert own progress"
  ON public.karmic_progress FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- 6. ANTI-SCRAPING PUBLIC LOCKDOWN
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon, public;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT USAGE ON SCHEMA public TO authenticated;
