import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent

# NOTE:todo daod passado para um db, deve ser passado em uma tupla ou uma lista para rodar

# NOTE:Comando para criar um arquivo sqlite(o banco de dados) dentro dos arquivos python
conexao = sqlite3.connect(ROOT_PATH / "meu_banco.db")
# NOTE:Comando para ativar o nosso "poder de edição" no nosso banco de dados
cursor = conexao.cursor()
# NOTE:Esse comando, faz com que a linha que você passou, seja filtrada para um objeto da API integrada do python, transformando toda a tupla em um dicionario, facilitando na exibição dos dados, exibição mais limpa do código, e fazendo com que o acesso a esses dados seja facilidado(transforma as colunas para que aquele dado pertence em chaves, e os dados em valores)
cursor.row_factory = sqlite3.Row


def criar_tabela(conexao, cursor):
    # NOTE:o.execute serve para executarmos um comando, usando o comando CREATE TABLE "nome_da_tabela"("nome_da_coluna" e o tipo da coluna)
    # NOTE:na hora da criação de colunas na tabela, para definirmos uma primary key, definimos logo o tipo da primary key, e depois colocamos "PRIMARY KEY" e o "AUTOINCREMENT" para aumentar automaticamente o valor da nossa chave primaria.
    cursor.execute(
        "CREATE TABLE clientes(id INTEGER PRIMARY KEY AUTOINCREMENT, nome VARCHAR(100), email VARCHAR(150))"
    )


def inserir_dados(conexao, cursor, nome, email):
    data = (nome, email)
    # NOTE:Para você inserir linhas para a sua tabela, precisamos usar o comando, INSERT INTO "nome_da_tabela"("colunas") VALUES (?, ?)[isso para adicionar valores como uma tupla e de maneira mais segura para o SGDB];", variavel[deve ser uma tupla com os valores que você quer adicionar, ou variaveis com os valores que você quer adicionar, mas devem estar dentro de uma tupla no comando]
    cursor.execute("INSERT INTO clientes(nome, email) VALUES (?, ?);", data)
    # NOTE:Devemos usar a conexao com o banco de dados para lançar as alterações que fizemos nele, todos as alterações utilizadas com o cursor ficam "dentro" da variavel q conecta o compilador com o banco de dados, e para mandar as alterações para o banco de dados, devemos usar o comando .commit()
    conexao.commit()


def atualizar_registro(conexao, cursor, nome, email, id):
    data = (nome, email, id)
    # NOTE:O comando em SQL para modificar uma certa linha da minha tabela, é UPDATE nome da tabela SET "nome das colunas que você quer modificar", WHERE primary-key(para modificar apenas a linha espécifica que você quer atualizar)
    cursor.execute("UPDATE clientes SET nome = ?, email = ? WHERE id = ?", data)
    conexao.commit()


def deletar(conexao, cursor, id):
    data = (id,)
    # NOTE:O comando em SQL para deletar uma linha da minha tabela, é DELETE FROM nome da tabela, e você a partir dái pode excluir algumas colunas só ou a linha inteira, e sempre coloque o WHERE primary-key, para localizar a exata linha que você quer excluir do seu banco.
    cursor.execute("DELETE FROM clientes WHERE id = ?", data)
    conexao.commit()


def inserir_muitos(conexao, cursor, dados):
    # NOTE:O comando em sql para executar varios comandos de uma vez, é apenas você usar o comando executemany com o cursor
    cursor.executemany("INSERT INTO clientes (nome, email) VALUES (?,?)", dados)
    conexao.commit()


def exibir_dado(cursor, dados):
    # NOTE:o metodo fetchone, pega uma linha especifica da tabela para exibila no terminal, e sempre retorna uma tupla com os dados que você definiu no comando sql, podendo ser todos ou dados mais espécificos(como apenas uma coluna ou n colunas)
    cursor.execute("SELECT * FROM clientes WHERE id = ?;", (dados,))
    return cursor.fetchone()


def exibir_dados(cursor):
    # NOTE:faz a mesma coisa que o fetchone, mas diferente de retornar apenas uma linha, ele retorna uma lista q dentro dela, possui tuplas de cada linha da sua tabela que você determinou
    cursor.execute("SELECT * FROM clientes")
    print(cursor.fetchall())
    return cursor.fetchall()


cliente = exibir_dado(cursor, 2)
# NOTE:Quando você usar o comando row_factory no cursor, sempre exiba os dados recolhidos em formato de dicionario, para não retornar que o objeto cliente é uma instância de Row
print(dict(cliente))

# NOTE:Para proteger os seus dados, nunca instâncie como string um local de comando sql, sempre passe por fora do comando a tupla com os valores que você quer modificar, deletar ou fazer algo do tipo


