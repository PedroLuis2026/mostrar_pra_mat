import sqlite3
from pathlib import Path


def main():
    ROOT_PATH = Path("atv_IA")
    ROOT_PATH.mkdir(exist_ok=True)
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS usuario_sistema(id INTEGER PRIMARY KEY AUTOINCREMENT, cpf TEXT(11) UNIQUE, nome TEXT(100));")

    novos_usuarios = [
        ("111.222.333-44", "Alice Oliveira"),
        ("555.666.777-88", "Bruno Souza"),
        ("999.888.777-66", "Carla Dias"),
        ("111.222.333-44", "Alice Repetida"),
        ("222.333.444-55", "Daniel Lima"),
        ("555.666.777-88", "Bruno Clonado"),
        ("444.555.666-77", "Eduarda Melo")
    ]   
    #NOTE: O executemany ele salva tudo de uma vez, assim a gente pode usar o comando "OR IGNORE" para fazer com que ele ignore celulas de cpf iguais, não adicionando essa linha à tabela.
    #NOTE: Se a gente fosse fazer por execute, a gente teria que fazer um loop na lista que passamos dos dados, para adicionar um por um e fazer um commit específico para cada um deles, gastando mais memória consequentimente. 
    try:
        cursor.executemany("INSERT OR IGNORE INTO usuario_sistema(cpf,nome) VALUES(?,?);", novos_usuarios)
        conexao.commit()
    except Exception as e:
        print(f"Cadastro duplicado: {e}")
        conexao.rollback()
    conexao.close()
if __name__ == "__main__":
    main()