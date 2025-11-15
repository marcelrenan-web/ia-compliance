-- SQL para criar a tabela 'denuncias' (Postgres/Supabase)
CREATE TABLE IF NOT EXISTS denuncias (
    id TEXT PRIMARY KEY,
    setor TEXT,
    tipo_ocorrencia TEXT,
    descricao TEXT,
    data_envio TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
