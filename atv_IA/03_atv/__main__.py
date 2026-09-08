import sqlite3
from pathlib import Path


def main():

    ROOT_PATH = Path("atv_IA")
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS vendas(id_venda INTEGER PRIMARY KEY AUTOINCREMENT, regiao TEXT(100), valor_total DOUBLE(20,2), status_pagamento TEXT(9));"
    )
    dados = []
    for i in range(0, 3):
        dado = input("Digite o dado a seguir:")
        dados.append(dado)
    dados[1] = float(dados[1])
    dados = tuple(dados)

    dados_vendas = [
        ("Nordeste", 1500.50, "Aprovado"),
        ("Sudeste", 4200.00, "Aprovado"),
        ("Sul", 850.00, "Pendente"),
        ("Centro-Oeste", 2300.75, "Cancelado"),
        ("Norte", 980.00, "Aprovado"),
        ("Sudeste", 5100.20, "Pendente"),
        ("Nordeste", 3100.00, "Aprovado"),
        ("Sul", 1250.40, "Aprovado"),
        ("Centro-Oeste", 450.00, "Pendente"),
        ("Sudeste", 7200.10, "Aprovado"),
    ]
    cursor.execute(
        "INSERT INTO vendas(regiao,valor_total,status_pagamento) VALUES(?,?,?);", dados
    )
    conexao.commit()
    valores = query(cursor)

    for valor in valores:
        print("=" * 30)
        valor = dict(valor)
        for k, v in valor.items():
            print(f"{k}:  {v}")
    conexao.close()


def query(cursor):
    cursor.execute(
        "SELECT * FROM vendas WHERE regiao = 'Sudeste' AND valor_total > 1500 AND status_pagamento = 'Aprovado'"
    )
    resultado = cursor.fetchall()
    return resultado


if __name__ == "__main__":
    main()
