import sqlite3
from datetime import *
from pathlib import Path


def main():
    ROOT_PATH = Path("atv_IA")
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()
    cursor.row_factory = sqlite3.Row

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS logs_acesso(id_log INTEGER PRIMARY KEY AUTOINCREMENT, usuario_id INTEGER(20), data_acesso DATE, status_conta TEXT(15));"
    )

    hoje = datetime.now()
    data_antiga_1 = hoje - timedelta(days=120)
    data_antiga_2 = hoje - timedelta(days=95)
    data_recente = hoje - timedelta(days=5)

    dados_logs = [
        (101, data_antiga_1, "Ativa"),
        (102, data_recente, "Ativa"),
        (103, data_antiga_2, "Bloqueada"),
        (104, data_recente, "Cancelada"),
    ]

    cursor.executemany(
        "INSERT INTO logs_acesso(usuario_id, data_acesso, status_conta) VALUES(?,?,?)",
        dados_logs,
    )
    # NOTE:método usando o id para verificar
    logs = query(cursor)
    logs_excluir = []
    for log in logs:
        log = dict(log)
        if log["status_conta"] == "Cancelada":
            id = log["id_log"]
            logs_excluir.append((id,))
    # NOTE:Usando o metodo de cancelar diretamente pelo status_conta
    cursor.execute("DELETE FROM logs_acesso WHERE status_conta = 'Cancelada'")
    conexao.commit()
    conexao.close()


def query(cursor):
    cursor.execute("SELECT * FROM logs_acesso")
    resultado = cursor.fetchall()
    return resultado


if __name__ == "__main__":
    main()
