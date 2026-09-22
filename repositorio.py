"""Acesso ao banco de dados. Todo o SQL do projeto fica aqui e em mais
nenhum lugar — o menu nunca escreve uma query. Isso permite trocar o
SQLite por outro banco mexendo só neste arquivo."""

import sqlite3

ARQUIVO_BANCO = "estoque.db"


def conectar():
    conexao = sqlite3.connect(ARQUIVO_BANCO)
    conexao.row_factory = sqlite3.Row    # permite acessar a coluna pelo nome: linha['nome']
    return conexao


def criar_tabela():
    """Cria a tabela se ainda não existir. Seguro chamar a cada execução."""
    with conectar() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS produtos (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                nome      TEXT    NOT NULL,
                categoria TEXT    NOT NULL,
                estoque   INTEGER NOT NULL DEFAULT 0 CHECK (estoque >= 0),
                preco     REAL    NOT NULL CHECK (preco >= 0)
            )
        """)


def inserir(nome, categoria, estoque, preco):
    """Insere um produto e devolve o ID gerado pelo banco."""
    with conectar() as conexao:
        # Os valores vão na tupla, nunca concatenados no SQL:
        # é isso que impede SQL injection.
        cursor = conexao.execute(
            "INSERT INTO produtos (nome, categoria, estoque, preco) VALUES (?, ?, ?, ?)",
            (nome, categoria, estoque, preco),
        )
        return cursor.lastrowid


def listar():
    with conectar() as conexao:
        return conexao.execute("SELECT * FROM produtos ORDER BY id").fetchall()


def buscar_por_id(id_produto):
    """Devolve o produto, ou None se o ID não existir."""
    with conectar() as conexao:
        return conexao.execute(
            "SELECT * FROM produtos WHERE id = ?", (id_produto,)
        ).fetchone()


def atualizar(id_produto, nome, categoria, estoque, preco):
    with conectar() as conexao:
        # A ordem da tupla segue a ordem dos ? no SQL — o id vai por último
        # porque o WHERE aparece no fim da query.
        conexao.execute(
            "UPDATE produtos SET nome = ?, categoria = ?, estoque = ?, preco = ? "
            "WHERE id = ?",
            (nome, categoria, estoque, preco, id_produto),
        )


def deletar(id_produto):
    with conectar() as conexao:
        conexao.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
