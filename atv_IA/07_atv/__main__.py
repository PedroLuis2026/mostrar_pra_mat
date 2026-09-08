import sqlite3
from pathlib import Path


def main():
    ROOT_PATH = Path("atv_IA")
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()
    cursor.row_factory = sqlite3.Row
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS veiculos(id INTEGER PRIMARY KEY AUTOINCREMENT, placa VARCHAR(8), modelo VARCHAR(50));"
    )

    # NOTE:para fazer uma fk(chave estrangeira) em uma tabela sql, devemos fazer o seguinte comando após declarar o tipo da coluna, FOREIGN KEY (nome da coluna que irá ficar como chave estrangeira) REFERENCES nome_da_tabela(nome da primary-key)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS manutencoes(id INTEGER PRIMARY KEY AUTOINCREMENT, veiculo_id INTEGER(20), data VARCHAR(10), tipo_servico TEXT(50), FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE CASCADE) ;"
    )  # NOTE: O comando ON DELETE CASCADE, força o delete de todas as linhas q o id "pai" for apagado, a id "filha" apagar também.
    cursor.execute("DELETE FROM veiculos")
    cursor.execute("DELETE FROM manutencoes")
    conexao.commit()
    dados_veiculos = [
    ("ABC-1234", "Toyota Hilux"),
    ("XYZ-5678", "Chevrolet Onix"),
    ("MNO-9012", "Volkswagen Gol")
    ]
    try:
        cursor.executemany("INSERT INTO veiculos(placa,modelo) VALUES(?,?);", dados_veiculos)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro:{e}")
        conexao.rollback()    
    ids = {linha["modelo"]: linha["id"] for linha in cursor.execute("SELECT id, modelo FROM veiculos;").fetchall()}
    dados_manutencoes = [
    (ids["Toyota Hilux"], "2026-08-10", "Troca de óleo e filtro"),
    (ids["Toyota Hilux"], "2026-09-01", "Alinhamento e balanceamento"),
    (ids["Chevrolet Onix"], "2026-08-15", "Substituição das pastilhas de freio"),
    (ids["Volkswagen Gol"], "2026-09-05", "Revisão do sistema elétrico")
]
    try:
        cursor.executemany("INSERT INTO manutencoes(veiculo_id,data,tipo_servico) VALUES(?,?,?);", dados_manutencoes)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro:{e}")
        conexao.rollback()
    selecao = cursor.execute("SELECT veiculos.placa,veiculos.modelo,manutencoes.tipo_servico FROM veiculos INNER JOIN manutencoes ON veiculos.id = manutencoes.veiculo_id").fetchall()
    for situ in selecao:
        print("=" * 30)
        print(f"Placa do veículo:   {situ["placa"]}\nModelo:   {situ["modelo"]}\nTipo do serviço:   {situ["tipo_servico"]}")
    


if __name__ == "__main__":
    main()