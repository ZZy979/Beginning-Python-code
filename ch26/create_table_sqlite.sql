CREATE TABLE messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    subject     TEXT NOT NULL,
    sender      TEXT NOT NULL,
    reply_to    INT,
    text        TEXT NOT NULL
);