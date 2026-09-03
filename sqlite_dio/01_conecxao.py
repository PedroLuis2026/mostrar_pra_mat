import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

# Comando para criar um arquivo sqlite(o banco de dados) dentro dos arquivos python
conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")
# Comando para ativar o nosso "poder de edição" no nosso banco de dados
cursor = conexao.cursor()

# o.execute serve para executarmos um comando, usando o comando CREATE TABLE "nome_da_tabela"("nome_da_coluna" e o tipo da coluna)
# NOTE: na hora da criação de colunas na tabela, para definirmos uma primary key, definimos logo o tipo da primary key, e depois colocamos "PRIMARY KEY" e o "AUTOINCREMENT" para aumentar automaticamente o valor da nossa chave primaria. 
#cursor.execute("CREATE TABLE clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))")

data = ("Alana", "Lana@gmail.com")
# Para você inserir linhas para a sua tabela, precisamos usar o comando, INSERT INTO "nome_da_tabela"("colunas") VALUES (?, ?)[isso para adicionar valores como uma tupla e de maneira mais segura para o SGDB];", variavel[deve ser uma tupla com os valores que você quer adicionar, ou variaveis com os valores que você quer adicionar, mas devem estar dentro de uma tupla no comando]
cursor.execute("INSERT INTO clientes(nome, email) VALUES (?, ?);", data)
# Devemos usar a conexao com o banco de dados para lançar as alterações que fizemos nele, todos as alterações utilizadas com o cursor ficam "dentro" da variavel q conecta o compilador com o banco de dados, e para mandar as alterações para o banco de dados, devemos usar o comando .commit() 
conexao.commit()
