-- Eliminar tablas si existen
DROP TABLE IF EXISTS reports;
DROP TABLE IF EXISTS analyzed_content;
DROP TABLE IF EXISTS boe_entries;

-- Crear tablas
CREATE TABLE boe_entries (
    id SERIAL PRIMARY KEY,
    entry_id VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE analyzed_content (
    id SERIAL PRIMARY KEY,
    entry_id VARCHAR(255) REFERENCES boe_entries(entry_id),
    summary TEXT,
    keywords TEXT[],
    relevance_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    content_id INTEGER REFERENCES analyzed_content(id),
    summary TEXT,
    recipients TEXT[],
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejor rendimiento
CREATE INDEX idx_boe_entries_entry_id ON boe_entries(entry_id);
CREATE INDEX idx_analyzed_content_entry_id ON analyzed_content(entry_id); 