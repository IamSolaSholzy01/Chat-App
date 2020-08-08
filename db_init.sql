CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    message_id INTEGER PRIMARY KEY,
    dt TEXT NOT NULL,
    message TEXT NOT NULL,
    sender TEXT NOT NULL,
    recipient TEXT
);