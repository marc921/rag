-- name: InsertVerse :one
INSERT INTO verses (book, chapter, verse, content, embedding) VALUES ($1, $2, $3, $4, $5) RETURNING *;

-- name: GetVerse :one
SELECT * FROM verses WHERE id = $1;

-- name: GetSimilarVerses :many
SELECT * FROM verses ORDER BY embedding <=> $1 LIMIT $2;