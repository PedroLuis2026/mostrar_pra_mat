import sqlite3
from pathlib import Path

def main():
    global cursor, conexao
    ROOT_PATH = Path("atv_IA")
    ROOT_PATH.mkdir(exist_ok=True)
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS logar(usuario VARCHAR PRIMARY KEY, ip VARCHAR(30));")

    registrar_login("alice123", "192.168.1.10")
    auditar_acesso("alice123")
    registrar_login("alice123", "192.168.1.10")
    auditar_acesso("Pedrolas")

def conectar_db(ROTA):
    return sqlite3.connect(ROTA / "ecommerce.db")

def registrar_login(usuario, ip):
    dados = (usuario, ip)
    try:
        cursor.execute("INSERT INTO logar(usuario,ip) VALUES(?,?);", dados)
        conexao.commit()
    except Exception as e:
        print(f"O usuário já está registrado: {e}")
        conexao.rollback()

def auditar_acesso(usuario):
    usuario = (usuario,)
    ip = cursor.execute("SELECT ip FROM logar WHERE usuario = ?;", usuario).fetchone()
    if ip:
        print(f"O ip o usuário {usuario[0]} é {ip[0]}")
    else:
        print(f"O usuário {usuario[0]} não foi encontrado.")

if __name__ == "__main__":
    main()