-- name: ListUsers :many
SELECT * FROM users;

-- name: InsertUser :one
INSERT INTO users (name, hashed_password) VALUES ($1, $2) RETURNING *;

-- name: GetUser :one
SELECT * FROM users WHERE name = $1;