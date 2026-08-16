-- Bite Budget Supabase schema for San Antonio MVP
-- Run in Supabase SQL Editor

CREATE EXTENSION IF NOT EXISTS cube;
CREATE EXTENSION IF NOT EXISTS earthdistance;

CREATE TYPE location_type AS ENUM ('restaurant', 'grocery');
CREATE TYPE health_goal AS ENUM ('gain_muscle', 'lose_weight', 'maintain');

CREATE TABLE locations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  chain TEXT NOT NULL,
  type location_type NOT NULL,
  address TEXT NOT NULL,
  lat DOUBLE PRECISION NOT NULL,
  lng DOUBLE PRECISION NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE meals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  location_chain TEXT NOT NULL,
  type location_type NOT NULL,
  title TEXT NOT NULL,
  order_description TEXT NOT NULL,
  items JSONB DEFAULT '[]',
  recipe TEXT DEFAULT '',
  prep_minutes INT DEFAULT 0,
  base_price NUMERIC(6,2) NOT NULL,
  per_serving_price NUMERIC(6,2),
  calories INT NOT NULL,
  protein_g NUMERIC(5,1) NOT NULL,
  carbs_g NUMERIC(5,1) NOT NULL,
  fat_g NUMERIC(5,1) NOT NULL,
  goals health_goal[] NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_locations_chain ON locations(chain);
CREATE INDEX idx_meals_chain ON meals(location_chain);
CREATE INDEX idx_meals_goals ON meals USING GIN(goals);

-- Haversine distance in miles
CREATE OR REPLACE FUNCTION distance_miles(
  lat1 DOUBLE PRECISION,
  lng1 DOUBLE PRECISION,
  lat2 DOUBLE PRECISION,
  lng2 DOUBLE PRECISION
) RETURNS DOUBLE PRECISION AS $$
  SELECT 3959 * acos(
    LEAST(1.0, GREATEST(-1.0,
      cos(radians(lat1)) * cos(radians(lat2)) *
      cos(radians(lng2) - radians(lng1)) +
      sin(radians(lat1)) * sin(radians(lat2))
    ))
  );
$$ LANGUAGE SQL IMMUTABLE;

-- Tax-inclusive price check (8.25% SA rate)
CREATE OR REPLACE FUNCTION price_with_tax(price NUMERIC)
RETURNS NUMERIC AS $$
  SELECT ROUND(price * 1.0825, 2);
$$ LANGUAGE SQL IMMUTABLE;
