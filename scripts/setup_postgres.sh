#!/bin/bash

# Configuración de variables
DB_NAME="boe_db"
DB_USER="boe_user"
DB_PASSWORD="your_password"  # Cambia esto por una contraseña segura

# Añadir manejo de errores y verificación
if ! command -v psql &> /dev/null; then
    echo "Error: PostgreSQL no está instalado"
    exit 1
fi

# Crear usuario y base de datos con manejo de errores
if ! psql postgres -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null; then
    echo "El usuario ya existe o hubo un error al crearlo"
fi

if ! psql postgres -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null; then
    echo "La base de datos ya existe o hubo un error al crearla"
fi

# Crear las tablas necesarias
psql -U $DB_USER -d $DB_NAME <<EOF
CREATE TABLE IF NOT EXISTS boe_entries (
    id VARCHAR PRIMARY KEY,
    content TEXT,
    metadata JSONB,
    processed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS analyzed_content (
    entry_id VARCHAR REFERENCES boe_entries(id),
    summary TEXT,
    keywords TEXT[],
    relevance_score FLOAT
);

CREATE TABLE IF NOT EXISTS reports (
    content_id VARCHAR REFERENCES boe_entries(id),
    summary TEXT,
    recipients TEXT[],
    sent_at TIMESTAMP
);
EOF

if [ $? -eq 0 ]; then
    echo "Base de datos configurada correctamente"
else
    echo "Error al configurar las tablas"
    exit 1
fi 