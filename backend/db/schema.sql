CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    company TEXT,
    industry TEXT,
    website TEXT,
    email TEXT UNIQUE,
    linkedin TEXT,
    country TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    title TEXT,
    year INTEGER,
    pdf_path TEXT,
    FOREIGN KEY(author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS analysis (
    author_id INTEGER PRIMARY KEY,
    philosophy TEXT,
    principles TEXT,
    tone TEXT,
    beliefs TEXT,
    opportunities TEXT,
    FOREIGN KEY(author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS emails (
    author_id INTEGER PRIMARY KEY,
    subject TEXT,
    body_formal TEXT,
    body_friendly TEXT,
    body_short TEXT,
    selected_variant TEXT,
    status TEXT DEFAULT 'pending', -- pending, sent, failed, skipped
    last_sent_at TIMESTAMP,
    FOREIGN KEY(author_id) REFERENCES authors(id)
);

CREATE TABLE IF NOT EXISTS blacklist (
    email TEXT PRIMARY KEY,
    reason TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER,
    email_sent_to TEXT,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT,
    FOREIGN KEY(author_id) REFERENCES authors(id)
);
