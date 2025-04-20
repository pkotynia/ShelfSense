-- Schema for ShelfSense MVP

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create a dedicated schema
CREATE SCHEMA IF NOT EXISTS shelfsense;

SET search_path TO shelfsense;

-- Helper function to automatically update 'updated_at' timestamps
CREATE OR REPLACE FUNCTION shelfsense.trigger_set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Users table
CREATE TABLE shelfsense.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(254) NOT NULL UNIQUE,
    username VARCHAR(255) NOT NULL, -- Added username
    password_hash VARCHAR(60) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.users
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- Books table
CREATE TABLE shelfsense.books (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) NULL, -- ISBN is optional
    genre TEXT NULL, -- Added optional genre
    description TEXT NULL, -- Added optional description
    publication_date DATE NULL, -- Added optional publication date
    page_count INTEGER NULL, -- Added optional page count
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.books
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- User Preferences table (1-to-1 with users)
CREATE TABLE shelfsense.user_preferences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL UNIQUE REFERENCES shelfsense.users(id) ON DELETE CASCADE,
    preferences_text TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.user_preferences
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- User Library Entries table (Many-to-Many link between users and books)
CREATE TABLE shelfsense.user_library_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES shelfsense.users(id) ON DELETE CASCADE,
    book_id UUID NOT NULL REFERENCES shelfsense.books(id) ON DELETE RESTRICT, -- Prevent book deletion if in library
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, book_id) -- User can add a book only once
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.user_library_entries
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- Reviews table (1-to-1 with user_library_entries)
CREATE TABLE shelfsense.reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_library_entry_id UUID NOT NULL UNIQUE REFERENCES shelfsense.user_library_entries(id) ON DELETE CASCADE,
    review_text TEXT NOT NULL,
    -- Consider adding 'generated_by_ai BOOLEAN DEFAULT FALSE' if needed later
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.reviews
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- Recommendations table
CREATE TABLE shelfsense.recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES shelfsense.users(id) ON DELETE CASCADE,
    recommended_book_id UUID NOT NULL REFERENCES shelfsense.books(id) ON DELETE RESTRICT, -- Prevent book deletion if recommended
    -- Consider adding 'reason TEXT' or 'source_book_id UUID' later
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, recommended_book_id) -- Avoid duplicate recommendations
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.recommendations
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- Recommendation Ratings table
CREATE TABLE shelfsense.recommendation_ratings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recommendation_id UUID NOT NULL UNIQUE REFERENCES shelfsense.recommendations(id) ON DELETE CASCADE, -- Rating is 1-to-1 with recommendation
    user_id UUID NOT NULL REFERENCES shelfsense.users(id) ON DELETE CASCADE, -- Added user_id for RLS
    rating NUMERIC(2,1) NOT NULL CHECK (rating >= 1.0 AND rating <= 5.0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TRIGGER set_timestamp
BEFORE UPDATE ON shelfsense.recommendation_ratings
FOR EACH ROW
EXECUTE FUNCTION shelfsense.trigger_set_timestamp();

-- Indexes
CREATE INDEX idx_books_title ON shelfsense.books(title);
CREATE INDEX idx_user_preferences_user_id ON shelfsense.user_preferences(user_id);
CREATE INDEX idx_user_library_entries_user_id ON shelfsense.user_library_entries(user_id);
CREATE INDEX idx_user_library_entries_book_id ON shelfsense.user_library_entries(book_id);
CREATE INDEX idx_reviews_user_library_entry_id ON shelfsense.reviews(user_library_entry_id);
CREATE INDEX idx_recommendations_user_id ON shelfsense.recommendations(user_id);
CREATE INDEX idx_recommendations_recommended_book_id ON shelfsense.recommendations(recommended_book_id);
CREATE INDEX idx_recommendation_ratings_recommendation_id ON shelfsense.recommendation_ratings(recommendation_id);
CREATE INDEX idx_recommendation_ratings_user_id ON shelfsense.recommendation_ratings(user_id);

-- Row Level Security (RLS)

-- Helper function to get current user ID (replace with actual mechanism)
-- This is a placeholder. In a real app, you'd set this via SET LOCAL or similar.
CREATE OR REPLACE FUNCTION shelfsense.current_user_id()
RETURNS UUID AS $$
BEGIN
  RETURN current_setting('app.current_user_id', true)::uuid;
EXCEPTION
  WHEN UNDEFINED_OBJECT THEN
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Enable RLS for user-specific tables
ALTER TABLE shelfsense.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE shelfsense.user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE shelfsense.user_library_entries ENABLE ROW LEVEL SECURITY;
ALTER TABLE shelfsense.reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE shelfsense.recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE shelfsense.recommendation_ratings ENABLE ROW LEVEL SECURITY;

-- RLS Policies

-- Users can manage their own user record
CREATE POLICY user_manage_own ON shelfsense.users
    FOR ALL
    USING (id = shelfsense.current_user_id());

-- Users can manage their own preferences
CREATE POLICY user_manage_own_preferences ON shelfsense.user_preferences
    FOR ALL
    USING (user_id = shelfsense.current_user_id());

-- Users can manage their own library entries
CREATE POLICY user_manage_own_library_entries ON shelfsense.user_library_entries
    FOR ALL
    USING (user_id = shelfsense.current_user_id());

-- Users can manage reviews associated with their library entries
-- Note: This requires joining to check ownership indirectly
CREATE POLICY user_manage_own_reviews ON shelfsense.reviews
    FOR ALL
    USING (
        EXISTS (
            SELECT 1
            FROM shelfsense.user_library_entries ule
            WHERE ule.id = reviews.user_library_entry_id
            AND ule.user_id = shelfsense.current_user_id()
        )
    );

-- Users can view and delete their own recommendations
-- (Assuming recommendations are generated by the system, not inserted by users)
CREATE POLICY user_view_delete_own_recommendations ON shelfsense.recommendations
    FOR SELECT, DELETE
    USING (user_id = shelfsense.current_user_id());
-- Allow system/backend role to insert recommendations (adjust role name as needed)
-- CREATE POLICY system_insert_recommendations ON shelfsense.recommendations
--     FOR INSERT
--     WITH CHECK (current_user = 'backend_role'); -- Example, adjust role check

-- Users can manage their own recommendation ratings
CREATE POLICY user_manage_own_recommendation_ratings ON shelfsense.recommendation_ratings
    FOR ALL
    USING (user_id = shelfsense.current_user_id());


-- Grant usage on schema and objects to application role (replace 'app_user' with actual role)
-- GRANT USAGE ON SCHEMA shelfsense TO app_user;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA shelfsense TO app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA shelfsense TO app_user; -- If using sequences
-- GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA shelfsense TO app_user;


