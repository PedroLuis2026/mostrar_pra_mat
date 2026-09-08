import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row

# NOTE:Sempre trate erros quando você for fazer uma QUERY em um db, quando tiver um intuito de modificar algo dentro dele, porque se der algum tipo de erro na modificação, você pode rever ela usando o comando conexao.rollback(), para fazer com todas as mudanças do seu ultimo commit sejam revertidas
try:
    cursor.execute(
        "INSERT INTO clientes(nome,email) VALUES(?,?)", ("Teste2", "email@teste.com")
    )
    cursor.execute(
        "ISERT INTO clientes(id, nome, email) VALUES(?,?,?)",
        (2, "Teste3", "email@teste.com"),
    )
    # NOTE:Sempre use apenas commits no final da sua mudança no seu banco de dados, para não acarretar em uma mudança inesperada no mesmo
    conexao.commit()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
    conexao.rollback()
