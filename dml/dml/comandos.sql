INSERT INTO usuarios (login, senha) VALUES ('admin', '1234');
INSERT INTO diretores (nome, nacionalidade) VALUES ('Christopher Nolan', 'Britanico');

UPDATE filmes SET ano_lancamento = 2024 WHERE id_filme = 1;

DELETE FROM filmes WHERE id_filme = 2;