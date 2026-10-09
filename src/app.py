import psycopg2

from psycopg2 import Error


# ==========================================================
# CONEXÃO COM O BANCO
# ==========================================================

def conectar():

    try:
        connection = psycopg2.connect(
            user="postgres",
            password="vecna001",
            host="127.0.0.1",
            port="5432",
            database="app-filme"
        )

        return connection

    except Exception as error:
        print("Erro de conexao. Verifique o banco e a senha.")
        return None


# ==========================================================
# FUNÇÕES DE CADASTRO
# ==========================================================

def cadastrar_usuario(conn):

    print("\n--- NOVO USUARIO ---")

    u = input("Login: ")
    s = input("Senha: ")

    try:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO usuarios (login, senha) VALUES (%s, %s)",
            (u, s)
        )

        conn.commit()

        print("Usuario cadastrado!")

    except Exception:
        conn.rollback()
        print("Erro: Login ja existe.")


def cadastrar_diretor(conn):

    cursor = conn.cursor()

    print("\n--- NOVO DIRETOR ---")

    n = input("Nome: ")
    nac = input("Nacionalidade: ")

    try:

        cursor.execute(
            "INSERT INTO diretores (nome, nacionalidade) VALUES (%s, %s)",
            (n, nac)
        )

        conn.commit()

        print("Diretor cadastrado!")

    except Exception:
        conn.rollback()
        print("Erro ao cadastrar diretor.")


def cadastrar_filme(conn):

    cursor = conn.cursor()

    listar_diretores(conn)

    print("\n--- NOVO FILME ---")

    t = input("Titulo: ")
    a = input("Ano: ")
    d = input("ID do Diretor (veja lista acima): ")

    try:

        cursor.execute(
            """
            INSERT INTO filmes
            (titulo, ano_lancamento, id_diretor)
            VALUES (%s, %s, %s)
            """,
            (t, a, d)
        )

        conn.commit()

        print("Filme cadastrado!")

    except Exception:
        conn.rollback()
        print("Erro: Verifique o ID do diretor.")


# ==========================================================
# PROCEDURE
# REGISTRAR AVALIAÇÃO
# ==========================================================

def cadastrar_avaliacao(conn):

    listar_filmes_simples(conn)

    print("\n--- NOVA AVALIACAO ---")

    id_f = input("ID do filme: ")
    nota = input("Nota (0-10): ")
    coment = input("Comentario: ")

    try:

        cursor = conn.cursor()

        # Chamada da PROCEDURE criada no PostgreSQL
        cursor.execute(
            "CALL registrar_avaliacao(%s, %s, %s)",
            (id_f, nota, coment)
        )

        conn.commit()

        print("Avaliacao registrada com sucesso!")

    except Exception as error:

        conn.rollback()

        print("Erro ao registrar avaliacao.")
        print("Detalhes:", error)


# ==========================================================
# FUNÇÕES DE CONSULTA
# ==========================================================

def listar_diretores(conn):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM diretores ORDER BY id_diretor"
    )

    print("\n--- DIRETORES ---")

    for r in cursor.fetchall():

        print(
            f"ID: {r[0]} | Nome: {r[1]} | "
            f"Nacionalidade: {r[2]}"
        )


def listar_filmes_simples(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id_filme, titulo
        FROM filmes
        ORDER BY id_filme
        """
    )

    print("\n--- LISTA DE FILMES ---")

    for r in cursor.fetchall():

        print(
            f"ID: {r[0]} | Titulo: {r[1]}"
        )


def listar_inner(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT f.titulo, d.nome
        FROM filmes f
        INNER JOIN diretores d
            ON f.id_diretor = d.id_diretor
        """
    )

    print("\n--- FILMES E DIRETORES (INNER JOIN) ---")

    for r in cursor.fetchall():

        print(
            f"Filme: {r[0]} | Diretor: {r[1]}"
        )


def listar_left(conn):

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT f.titulo, a.nota, a.comentario
        FROM filmes f
        LEFT JOIN avaliacoes a
            ON f.id_filme = a.id_filme
        """
    )

    print("\n--- FILMES E NOTAS (LEFT JOIN) ---")

    for r in cursor.fetchall():

        nt = r[1] if r[1] is not None else "N/A"

        print(
            f"Filme: {r[0]} | "
            f"Nota: {nt} | "
            f"Coment: {r[2] or '-'}"
        )


# ==========================================================
# VIEW
# RELATÓRIO COMPLETO DE FILMES
# ==========================================================

def relatorio_view(conn):

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            SELECT
                id_filme,
                titulo,
                ano_lancamento,
                diretor,
                nacionalidade,
                nota,
                comentario
            FROM vw_relatorio_filmes
            ORDER BY titulo
            """
        )

        resultados = cursor.fetchall()

        print("\n==========================================")
        print("       RELATORIO COMPLETO DE FILMES")
        print("       DADOS VINDOS DA VIEW")
        print("==========================================")

        if not resultados:

            print("Nenhum filme encontrado.")

        else:

            for r in resultados:

                print("\n------------------------------------------")

                print(f"ID: {r[0]}")
                print(f"Filme: {r[1]}")
                print(f"Ano: {r[2]}")
                print(f"Diretor: {r[3]}")
                print(f"Nacionalidade: {r[4]}")

                if r[5] is not None:
                    print(f"Nota: {r[5]}")
                else:
                    print("Nota: Ainda nao avaliado")

                print(
                    f"Comentario: {r[6] or '-'}"
                )

    except Exception as error:

        print("Erro ao consultar a View.")
        print("Detalhes:", error)


# ==========================================================
# FUNCTION
# CONSULTAR MÉDIA DE UM FILME
# ==========================================================

def consultar_media_filme(conn):

    listar_filmes_simples(conn)

    print("\n--- MEDIA DE AVALIACAO ---")

    id_filme = input("Digite o ID do filme: ")

    try:

        cursor = conn.cursor()

        # Chamada da FUNCTION criada no PostgreSQL
        cursor.execute(
            "SELECT calcular_media_filme(%s)",
            (id_filme,)
        )

        resultado = cursor.fetchone()

        media = resultado[0]

        print(
            f"\nMedia de avaliacao do filme: {media}"
        )

    except Exception as error:

        print("Erro ao calcular a media.")
        print("Detalhes:", error)


# ==========================================================
# FUNÇÕES DE MANUTENÇÃO
# ==========================================================

def atualizar_filme(conn):

    cursor = conn.cursor()

    listar_filmes_simples(conn)

    i = input("\nID do filme para atualizar: ")
    a = input("Novo ano: ")

    try:

        cursor.execute(
            """
            UPDATE filmes
            SET ano_lancamento = %s
            WHERE id_filme = %s
            """,
            (a, i)
        )

        conn.commit()

        print("Atualizado!")

    except Exception as error:

        conn.rollback()

        print("Erro ao atualizar filme.")
        print("Detalhes:", error)


def excluir_filme(conn):

    cursor = conn.cursor()

    listar_filmes_simples(conn)

    i = input("\nID do filme para excluir: ")

    try:

        cursor.execute(
            "DELETE FROM filmes WHERE id_filme = %s",
            (i,)
        )

        conn.commit()

        print("Removido!")

    except Exception as error:

        conn.rollback()

        print("Erro ao excluir filme.")
        print("Detalhes:", error)


# ==========================================================
# LOGIN
# ==========================================================

def login(conn):

    print("\n=== LOGIN ===")

    u = input("Usuario: ")
    s = input("Senha: ")

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuarios
        WHERE login = %s
        AND senha = %s
        """,
        (u, s)
    )

    if cursor.fetchone():

        print(f"\nBem-vindo, {u}!")

        return True

    print("\nErro: Usuario ou senha incorretos!")

    return False


# ==========================================================
# MENU PRINCIPAL
# ==========================================================

def menu_principal():

    print("\n======== MENU PRINCIPAL ========")

    print("1. [CADASTROS] (Filmes, Diretores, Notas)")
    print("2. [RELATORIOS] (Listagens e Recursos do Banco)")
    print("3. [GESTAO] (Editar ou Excluir)")
    print("0. Sair")

    return input("Escolha uma categoria: ")


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

def main():

    conexao = conectar()

    if conexao:

        logado = False

        # ==========================================
        # LOGIN / CADASTRO
        # ==========================================

        while not logado:

            print("\n1. Login | 2. Criar Conta | 0. Sair")

            inicio = input("Opcao: ")

            if inicio == "1":

                if login(conexao):
                    logado = True

            elif inicio == "2":

                cadastrar_usuario(conexao)

            elif inicio == "0":

                conexao.close()

                return

        # ==========================================
        # SISTEMA
        # ==========================================

        while logado:

            op = menu_principal()

            # ======================================
            # CADASTROS
            # ======================================

            if op == "1":

                print("\n--- CADASTROS ---")

                print("1. Cadastrar Diretor")
                print("2. Cadastrar Filme")
                print("3. Adicionar Nota a Filme")
                print("0. Voltar")

                sub = input("Escolha: ")

                if sub == "1":

                    cadastrar_diretor(conexao)

                elif sub == "2":

                    cadastrar_filme(conexao)

                elif sub == "3":

                    cadastrar_avaliacao(conexao)

            # ======================================
            # RELATÓRIOS
            # ======================================

            elif op == "2":

                print("\n--- RELATORIOS ---")

                print("1. Lista de Diretores")
                print("2. Lista de Filmes (Simples)")
                print("3. Filmes e Diretores (INNER JOIN)")
                print("4. Filmes e Notas (LEFT JOIN)")
                print("5. Relatorio Completo de Filmes (VIEW)")
                print("6. Consultar Media de um Filme (FUNCTION)")
                print("0. Voltar")

                sub = input("Escolha: ")

                if sub == "1":

                    listar_diretores(conexao)

                elif sub == "2":

                    listar_filmes_simples(conexao)

                elif sub == "3":

                    listar_inner(conexao)

                elif sub == "4":

                    listar_left(conexao)

                elif sub == "5":

                    relatorio_view(conexao)

                elif sub == "6":

                    consultar_media_filme(conexao)

            # ======================================
            # GESTÃO
            # ======================================

            elif op == "3":

                print("\n--- GESTAO ---")

                print("1. Atualizar Ano de Filme")
                print("2. Excluir Filme")
                print("0. Voltar")

                sub = input("Escolha: ")

                if sub == "1":

                    atualizar_filme(conexao)

                elif sub == "2":

                    excluir_filme(conexao)

            # ======================================
            # SAIR
            # ======================================

            elif op == "0":

                print("Saindo...")

                break

        conexao.close()


# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    main()
```
