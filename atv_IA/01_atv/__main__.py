import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
cursor = conexao.cursor()
# NOTE:também uma boa prática para criação da tabela se ela não existir, e parte para uma verificação também, para garantir que a tabela exista
cursor.execute(
    "CREATE TABLE IF NOT EXISTS produtos(id INTEGER PRIMARY KEY AUTOINCREMENT, sku VARCHAR(40), nome_produto VARCHAR(100), preco DOUBLE(30, 2))"
)

produtos = [
    ("m-preto", "Mouse", 100.80),
    ("c-med-preta-p", "Camisa", 50.99),
    ("s-lar-branco-G", "short", 60.40),
]

cursor.executemany(
    "INSERT INTO produtos(sku,nome_produto,preco) VALUES(?,?,?)", produtos
)
conexao.commit()
# NOTE:Isso também é uma boa prática, para não manter a conexão do banco de dados aberta
conexao.close()
