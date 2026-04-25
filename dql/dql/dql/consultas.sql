SELECT f.titulo, d.nome 
FROM filmes f 
INNER JOIN diretores d ON f.id_diretor = d.id_diretor;

SELECT f.titulo, a.nota 
FROM filmes f 
LEFT JOIN avaliacoes a ON f.id_filme = a.id_filme;

SELECT * FROM filmes WHERE ano_lancamento > 2020 ORDER BY titulo ASC;