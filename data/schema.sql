DROP TABLE IF EXISTS journals;

CREATE TABLE journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,
    publisher TEXT,

    issn_print TEXT,
    issn_online TEXT,

    country TEXT,
    language TEXT,

    discipline TEXT,
    subdiscipline TEXT,

    indexing TEXT,
    quartile TEXT,

    apc REAL,
    apc_currency TEXT,

    open_access BOOLEAN,

    website TEXT,
    submission_url TEXT,

    match_keywords TEXT,

    last_updated TEXT
);