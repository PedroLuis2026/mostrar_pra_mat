import sqlite3
from pathlib import Path


def main():
    ROOT_PATH = Path("atv_IA")
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT(100), email VARCHAR(150));"
    )

    dados_clientes = [
        ("Ana Silva", "  ana.silva@email.com "),
        ("BRUNO COSTA", "BRUNO.COSTA@EMAIL.COM"),
        (" carla souza", "carla.souza@email.com"),
        ("Diego Lima", "diego.lima@ Email.com"),
        ("Elena Ribeiro", "elena.ribeiro@email.com   "),
        ("Fábio Santos ", " fabio.santos@email.com"),
        ("GABRIELA MELO", "Gabriela.Melo@Email.com"),
        ("Hugo Oliveira", "hugo.oliveira@email..com"),
        (" Isabela Frota", "isabela.frota@email.com"),
        ("João Victor", "joao.victor@email.com "),
    ]

    cursor.executemany("INSERT INTO clientes(nome,email) VALUES(?,?);", dados_clientes)
    dados = query(cursor)
    dados_limpos = []
    for dado in dados:
        id = dado[0]
        nome_limpo = dado[1].strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
        email_limpo = dado[2].strip().lower().replace(" ", "")
        dados_limpos.append((nome_limpo, email_limpo, id))
    cursor.executemany("UPDATE clientes SET nome = ?, email = ? WHERE id = ?;", dados_limpos)
    conexao.commit()
    conexao.close()

def query(cursor):
    cursor.execute("SELECT * FROM clientes")
    resultado = cursor.fetchall()
    return resultado


if __name__ == "__main__":
    main()
