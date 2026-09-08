import sqlite3
from pathlib import Path

def main():
    ROOT_PATH = Path("atv_IA")
    conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
    cursor = conexao.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS faturamento_mensal(mes TEXT PRIMARY KEY, receita REAL(20), despesas REAL(20));")

    dados_semestre = [
    ("Março/2026", 45000.00, 60000.00),
    ("Abril/2026", 52000.50, 58000.00),
    ("Maio/2026", 61000.00, 59500.00),
    ("Junho/2026", 75000.20, 68000.00),
    ("Julho/2026", 92000.00, 71000.00),
    ("Agosto/2026", 115000.80, 75000.00)
    ]
    try:
        cursor.executemany("INSERT INTO faturamento_mensal(mes,receita,despesas) VALUES(?,?,?);", dados_semestre)
        conexao.commit()
    except Exception as e:
        print(f"Ocorreu um erro:{e}")
        conexao.rollback()

    receitas = cursor.execute("SELECT SUM(receita) FROM faturamento_mensal;").fetchone()
    despesas = cursor.execute("SELECT SUM(despesas) FROM faturamento_mensal;").fetchone()
    lucro = receitas[0] - despesas[0]

    print(f"O lucro líquido global da empresa é de R${lucro:.2f}".replace(".", ","))
    conexao.close()
    

if __name__ == "__main__":
    main()