import sqlite3
from pathlib import Path 

def main():
    global conexao, cursor, ROOT_PATH
    ROOT_PATH = Path("atv_IA")
    ROOT_PATH.mkdir(exist_ok=True)
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS leads_comerciais(id INTEGER PRIMARY KEY, empresa VARCHAR(100), contato INTEGER(20), probabilidade_fechamento_pct REAL(20));")
    conexao.close()

    while True:
        print("<" + ("=" * 40) + ">")
        print("[1].Cadastrar novo lead comercial")
        print("[2].Listar funil de vendas atual")
        print("[3].Atualizar probabilidades de fechamento")
        print("[4].Remover lead")
        print("[5].Encerrar sistema")
        print("<" + ("=" * 40) + ">")
        escolha = input("Digite a sua opção: ").strip()
        if escolha not in ["1", "2", "3", "4", "5"] or not escolha:
            print("Digite uma opção válida")
            continue
        match escolha:
            case "1":#Cadastrar nova empresa
                inserir_db()
            case "2":#Listar funil de vendas
                listar_empresas()
            case "3":#Atualizar pobabilidade de fechamento diacordo com o id da empresa
                atualizar_probabilidade()
            case "4":#Remover lead deletando a empresa do db
                remover_empresa()
            case "5": #Encerramento do programa
                print("Obrigado por usar a minha aplicação, até mais!👋")
                break

def conectar_db(rota):
    return sqlite3.connect(rota / "ecommerce.db")

def inserir_db():
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()

    print("<" + ("=" * 40) + ">")
    while True:
        nome = input("\nDigite o nome da empresa: ").strip()
        if not nome:
            print("Digite um nome válido!")
            continue
        break
    while True:
        contato_raw = input("\nDigite o contato da empresa: ").strip()
        if not contato_raw or len(contato_raw) < 10:
            print("Digite um número válido!")
            continue
        contato = []
        for letra in contato_raw:
            if letra.isdigit():
                contato.append(letra)
        contato = "".join(contato)
        if len(contato) <= 0:
            print("Digite um número válido!")
            continue
        break
    while True:
        probabilidade_raw = input("\nDigite a probabilidade de fechamento da empresa: ").strip()
        probabilidade_raw = probabilidade_raw.replace(",", ".")
        if not probabilidade_raw or probabilidade_raw.count(".") > 1:
            print("Digite um número válido!")
            continue
        prob = []
        for i in probabilidade_raw:
            if i.isdigit() or i == ".":
                prob.append(i)
        try:
            probabilidade = float("".join(prob))
        except ValueError:
            print("Digite um número válido!")
            continue
        break
    dados = (nome,contato,probabilidade)
    cursor.execute("INSERT INTO leads_comerciais(empresa,contato,probabilidade_fechamento_pct) VALUES(?,?,?);", dados)
    conexao.commit()
    print("\nDados salvos no banco de dados!")
    print("<" + ("=" * 40) + ">")
    conexao.close()

def listar_empresas():
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()
    cursor.row_factory = sqlite3.Row
    empresas = cursor.execute("SELECT * FROM leads_comerciais").fetchall()
    if empresas:
        for empresa in empresas:
            empresa = dict(empresa)
            print("<" + ("=" * 40) + ">")
            print(f"\nID:     {empresa['id']}\nNOME DA EMPRESA:     {empresa['empresa']}\nCONTATO:     {empresa['contato']}\nPOSSIBILIDADE DE FECHAMENTO:     {empresa['probabilidade_fechamento_pct']:.2f}%")
        print("<" + ("=" * 40) + ">")
    else:
        print("<" + ("=" * 40) + ">")
        print("\nNenhuma empresa cadastrada\n")
        print("<" + ("=" * 40) + ">")
    conexao.close()

def atualizar_probabilidade():
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()

    print("<" + ("=" * 40) + ">")
    while True:
        iden = input("Digite o id da empresa: ").strip()
        if not iden or not iden.isdigit():
            print("Digite um id válido")
            continue
        iden = int(iden)
        break

    empresa = cursor.execute("SELECT empresa FROM leads_comerciais WHERE id = ?;", (iden,)).fetchone()
    if empresa:
        while True:
            probabilidade_raw = input("Digite a nova probabilidade de fechamento da empresa: ").strip()
            probabilidade_raw = probabilidade_raw.replace(",", ".")
            if not probabilidade_raw or probabilidade_raw.count(".") > 1:
                print("Digite um número válido!")
                continue
            prob = []
            for i in probabilidade_raw:
                if i.isdigit() or i == ".":
                    prob.append(i)
            probabilidade = float("".join(prob))
            break   
        cursor.execute("UPDATE leads_comerciais SET probabilidade_fechamento_pct = ? WHERE id = ?", (probabilidade,iden))
        conexao.commit()
        print(f"A possibilidade  da empresa {empresa[0]}, foi atualizada com sucesso!")
    else:
        print("id não reconhecido.")
    print("<" + ("=" * 40) + ">")
    conexao.close()

def remover_empresa():
    conexao = conectar_db(ROOT_PATH)
    cursor = conexao.cursor()

    print("<" + ("=" * 40) + ">")
    while True:
        iden = input("Digite o id da empresa que você quer deletar: ").strip()
        if not iden or not iden.isdigit():
            print("Digite um id válido")
            continue
        iden = int(iden)
        break

    empresa = cursor.execute("SELECT empresa FROM leads_comerciais WHERE id = ?;", (iden,)).fetchone()
    if empresa: 
        cursor.execute("DELETE FROM leads_comerciais WHERE id = ?;", (iden,))
        conexao.commit()
        print(f"A empresa {empresa[0]} foi vendida com sucesso!")
    else:
        print("id não reconhecido.")
    print("<" + ("=" * 40) + ">")
    conexao.close()