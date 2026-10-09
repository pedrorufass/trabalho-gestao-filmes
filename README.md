# Sistema de Gestão de Filmes 🎬

### Descrição

Este projeto é uma aplicação de gestão de catálogo cinematográfico que permite o cadastro de usuários, diretores, filmes e avaliações. O sistema foi desenvolvido em Python integrado a um banco de dados PostgreSQL, com o objetivo de demonstrar conhecimentos em Banco de Dados, consultas SQL e integração entre aplicação e banco de dados.

Além das operações básicas de cadastro, consulta, atualização e exclusão, o sistema utiliza recursos avançados do PostgreSQL, como **View, Function e Procedure**, integrados diretamente às funcionalidades da aplicação.

### Tecnologias Utilizadas

* **Linguagem:** Python 3.x

* **Banco de Dados:** PostgreSQL

* **Biblioteca:** `psycopg2`

* **Ambiente:** VS Code

### Funcionalidades

* Cadastro e login de usuários;
* Cadastro de diretores;
* Cadastro de filmes;
* Cadastro de avaliações de filmes;
* Consulta de filmes e diretores;
* Consulta de filmes e avaliações;
* Atualização do ano de lançamento de filmes;
* Exclusão de filmes;
* Relatório completo de filmes utilizando uma **View**;
* Consulta da média de avaliações utilizando uma **Function**;
* Registro de avaliações utilizando uma **Procedure**.

### Recursos de Banco de Dados

O projeto utiliza os seguintes recursos solicitados na disciplina:

**View — `vw_relatorio_filmes`**

Responsável por reunir informações dos filmes, diretores e avaliações em uma única consulta. A View é utilizada pela aplicação para apresentar um relatório completo dos filmes.

**Function — `calcular_media_filme`**

Recebe o ID de um filme e calcula a média das avaliações cadastradas para ele. A Function é chamada pela aplicação para apresentar a média de avaliação de um filme.

**Procedure — `registrar_avaliacao`**

Responsável por registrar uma nova avaliação para um filme. A aplicação chama a Procedure ao realizar o cadastro de uma avaliação.

### Estrutura do Repositório

* `/diagrama`: Diagrama Entidade-Relacionamento (DER).

* `/ddl`: Scripts de criação das tabelas (Data Definition Language).

* `/dml`: Scripts de inserção e manipulação de dados (Data Manipulation Language).

* `/dql`: Consultas SQL, incluindo consultas com `JOIN`, View e Function (Data Query Language).

* `/recursos_avancados`: Scripts contendo a criação da View, Function e Procedure utilizadas pelo sistema.

* `/src`: Código-fonte da aplicação Python.

### Integração Python + PostgreSQL

A aplicação Python utiliza a biblioteca `psycopg2` para realizar a conexão com o PostgreSQL e executar operações diretamente no banco de dados.

Os recursos avançados são utilizados da seguinte forma:

* **View:** consultada pela aplicação para gerar o relatório completo de filmes;
* **Function:** chamada pela aplicação para calcular a média de avaliações de um filme;
* **Procedure:** executada pela aplicação para registrar uma nova avaliação.

### Link do vídeo

