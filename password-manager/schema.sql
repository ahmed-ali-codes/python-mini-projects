DROP TABLE IF EXISTS entries;

CREATE TABLE entries (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    site      TEXT    NOT NULL,
    username  TEXT    NOT NULL,
    password  TEXT    NOT NULL,  -- stored as Fernet-encrypted ciphertext
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
