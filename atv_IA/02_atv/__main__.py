import sqlite3
from pathlib import Path

ROOT_PATH = Path("atv_IA")

conexao = sqlite3.connect(ROOT_PATH / "ecommerce.db")
cursor = conexao.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS funcionarios(id INTEGER PRIMARY KEY AUTOINCREMENT, matricula INTEGER(20), nome VARCHAR(100), cargo VARCHAR(100), salario DOUBLE(30,2));"
)

novos_contratados = [
    (1001, "Ana Silva", "Desenvolvedora Python Senior", 9500.00),
    (1002, "Bruno Costa", "Analista de Dados Pleno", 6200.00),
    (1003, "Carla Souza", "Gerente de Projetos", 11000.00),
    (1004, "Diego Lima", "Suporte Técnico Junior", 3000.00),
    (1005, "Elena Ribeiro", "Designer UX/UI Pleno", 5800.00),
    (1006, "Fábio Santos", "Engenheiro de DevOps", 8900.00),
    (1007, "Gabriela Melo", "Coordenadora de RH", 7500.00),
    (1008, "Hugo Oliveira", "Cientista de Dados Senior", 12000.00),
    (1009, "Isabela Frota", "Assistente Administrativo", 2800.00),
    (1010, "João Victor", "Desenvolvedor Frontend Junior", 3500.00),
]

cursor.executemany(
    "INSERT INTO funcionarios(matricula,nome,cargo,salario) VALUES(?,?,?,?);",
    novos_contratados,
)
# NOTE: o comando DROP TABLE, serve para apagar uma tabela inteira dentro do seu SGBD
# cursor.execute("DROP TABLE funcionarios")
conexao.commit()
