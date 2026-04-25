CREATE TABLE usuarios (
    id_usuario SERIAL PRIMARY KEY,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(50) NOT NULL
);

CREATE TABLE diretores (
    id_diretor SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50)
);

CREATE TABLE filmes (
    id_filme SERIAL PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    ano_lancamento INT,
    id_diretor INT,
    CONSTRAINT fk_diretor FOREIGN KEY (id_diretor) REFERENCES diretores(id_diretor) ON DELETE CASCADE
);

CREATE TABLE avaliacoes (
    id_avaliacao SERIAL PRIMARY KEY,
    id_filme INT,
    nota DECIMAL(3,1) CHECK (nota >= 0 AND nota <= 10),
    comentario TEXT,
    CONSTRAINT fk_filme FOREIGN KEY (id_filme) REFERENCES filmes(id_filme) ON DELETE CASCADE
);