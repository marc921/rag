-- migrate:up
CREATE EXTENSION IF NOT EXISTS "vector";

CREATE TABLE verses (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v1(),
  book TEXT,
  chapter INT,
  verse INT,
  content TEXT NOT NULL,
  embedding vector(768) NOT NULL,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down
DROP TABLE verses;
