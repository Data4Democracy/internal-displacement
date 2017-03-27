DROP TYPE IF EXISTS status CASCADE;
CREATE TYPE status AS ENUM ('new', 'fetching', 'fetched',
    'processing', 'processed', 'fetching failed', 'processing failed');

DROP TYPE IF EXISTS category CASCADE;
CREATE TYPE category AS ENUM ('other', 'disaster', 'conflict');

DROP TABLE IF EXISTS article CASCADE;
CREATE TABLE article (
    id SERIAL PRIMARY KEY,
    url TEXT UNIQUE NOT NULL,
    domain TEXT,
    status status,
    title TEXT,
    publication_date TIMESTAMP,
    authors TEXT,
    language CHAR(2),
    relevance BOOL,
    reliability DECIMAL
);

DROP TABLE IF EXISTS content CASCADE;
CREATE TABLE content (
    article INT PRIMARY KEY REFERENCES article ON DELETE CASCADE,
    retrieval_date TIMESTAMP,
    content TEXT,
    content_type TEXT
);

DROP TABLE IF EXISTS article_category CASCADE;
CREATE TABLE article_category (
    article INT REFERENCES article ON DELETE CASCADE,
    category category,
    PRIMARY KEY (article, category)
);

DROP TABLE IF EXISTS country CASCADE;
CREATE TABLE country (
    code CHAR(3) PRIMARY KEY
);

DROP TABLE IF EXISTS country_term CASCADE;
CREATE TABLE country_term (
    term TEXT PRIMARY KEY,
    country CHAR(3) REFERENCES country ON DELETE CASCADE
);

DROP TABLE IF EXISTS location CASCADE;
CREATE TABLE location (
    id SERIAL PRIMARY KEY,
    description TEXT,
    country CHAR(3) REFERENCES country ON DELETE CASCADE,
    latlong TEXT
);

DROP TABLE IF EXISTS report CASCADE;
CREATE TABLE report (
    id SERIAL PRIMARY KEY,
    article INT REFERENCES article ON DELETE CASCADE,
    event_term TEXT,
    subject_term TEXT,
    quantity INT,
    tag_locations JSON,
    accuracy DECIMAL,
    analyzer TEXT,
    analysis_date TIMESTAMP WITH TIME ZONE
);

DROP TABLE IF EXISTS report_location CASCADE;
CREATE TABLE report_location (
    report INT REFERENCES report ON DELETE CASCADE,
    location INT REFERENCES location ON DELETE CASCADE,
    PRIMARY KEY (report, location)
);

DROP TABLE IF EXISTS report_datespan CASCADE;
CREATE TABLE report_datespan (
    id SERIAL PRIMARY KEY,
    report INT REFERENCES report ON DELETE CASCADE,
    start TIMESTAMP,
    finish TIMESTAMP
);


