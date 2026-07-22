DROP TABLE IF EXISTS journals;

CREATE TABLE journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    title TEXT NOT NULL,

    publisher TEXT,
    country TEXT,

    website TEXT,
    doaj_url TEXT,

    issn_print TEXT,
    issn_online TEXT,

    subjects TEXT,
    keywords TEXT,
    languages TEXT,

    apc TEXT,
    apc_amount REAL,
    waiver_policy TEXT,

    review_process TEXT,
    review_weeks INTEGER,

    license TEXT,

    article_count INTEGER,

    source TEXT
);