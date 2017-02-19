DROP TABLE IF EXISTS Labels;
DROP TABLE IF EXISTS Articles;

CREATE TABLE Articles (
    url TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    publish_date TIMESTAMP,
    domain TEXT,
    content TEXT,
    content_type TEXT,
    language TEXT
);


CREATE TABLE Labels (
    url TEXT REFERENCES Articles,
    category TEXT
)
