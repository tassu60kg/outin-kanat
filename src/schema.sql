CREATE TABLE bib_references (
    id SERIAL PRIMARY KEY,
    cite_key TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    title TEXT NOT NULL,
    author TEXT,
    year INTEGER,
    booktitle TEXT,
    journal TEXT,
    publisher TEXT,
    volume TEXT,
    pages TEXT,
    ISBN TEXT
);