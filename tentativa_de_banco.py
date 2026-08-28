from random import randint
from datetime import *
from abc import *

class Banco:
    def __init__(self, nome_banco:str):
        self.nome_banco = nome_banco
        self.__lista_contas = []
        self.__lista_clientes = []
        self.agencia = "00001"

    @property
    def historico(self):
        return self.__historico

    @property
    def lista_clientes(self):
        return self.__lista_clientes

    @property
    def lista_contas(self):
        return self.__lista_contas
    
    def registrar_cliente(self):
        self.__lista_clientes.append(gerar_cliente())
        print("\nCliente cadastrado com sucesso!")

    def abrir_conta(self):
        while True:
            cpf = input("\nDigite o seu cpf(apenas números): ").strip()
            if not cpf:
                print("\nDigite algo válido")
                continue
            break

        cliente_encontrado = None
        for cliente_ in self.__lista_clientes:
            if cpf == cliente_.cpf:
                cliente_encontrado = cliente_
                break
        if not cliente_encontrado:
            print("\nO cliente não está registrado no banco.")
            return
        for conta_ in self.__lista_contas:
            if cpf == conta_.cliente.cpf:
                print("\nO cliente não pode possuir mais de uma conta.")
                return
        tipo_conta = cliente_encontrado.solicitar_conta()
        
        numeros = "".join([str(randint(0,9)) for _ in range(0,6)])
        agencia = f"{self.agencia}{Cliente.total_conta}"
        if tipo_conta == "conta-comum":
            conta = Conta(agencia=agencia, numero=numeros, cliente=cliente_encontrado)
        if tipo_conta == "conta-corrente":
            conta = ContaCorrente(agencia=agencia, numero=numeros, cliente=cliente_encontrado)
        self.__lista_contas.append(conta)
        print(f"\nA {tipo_conta} de número {conta.numero_conta} foi criada com sucesso!")
    def solicitacao(self):
        while True:
            cpf = input("\nDigite o seu cpf(apenas números): ").strip()
            if not cpf:
                print("\nDigite algo válido")
                continue
            break
        for conta in self.__lista_contas:
            if cpf == conta.cliente.cpf:
                cliente = conta.cliente
                return cliente.solicitar_transacao(conta)
        print("\nCPF inválido ou conta não encontrada")

    def listar_contas(self):
           print("=" * 40)
           print("CONTAS".center(40))
           print("=" * 40)
           if len(self.__lista_contas) == 0:
               print("\nNenhuma conta foi criada ainda.")
               return
           for conta in self.__lista_contas:
               print(f"\nDono:\t{conta.cliente.nome}\nAgência:\t{conta.agencia}\nNúmero:\t{conta.numero_conta}\n")
               print("=" * 40)
class Cliente:
    total_conta = 0
    def __init__(self, nome:str, cpf:str, endereco:str):
        self.nome = nome
        self.cpf = cpf
        self.endereco = endereco
        Cliente.total_conta += 1

    def solicitar_conta(self):
        while True:
            tipo_conta = input("\nQual tipo de conta você quer criar? [conta-comum] [conta-corrente] ").strip().lower()
            if not tipo_conta or tipo_conta not in ["conta-comum", "conta-corrente"]:
                print("\nDigite algo válido")
                continue
            break
        return tipo_conta

    def solicitar_tansacao(self, conta):
        while True:
            escolha = input("\nQue tipo de transação você quer fazer? [sacar] [depositar]").strip().lower()
            if not escolha or escolha not in ["sacar", "depositar"]:
                print("\nDigite algo válido")
                continue
            break

        while True:
            try:
                valor = float(input(f"\nDigite o valor que você quer {"sacar" if escolha == "sacar" else "depositar"} {"da" if escolha == "sacar" else "na"} conta: "))
                if valor <= 0:
                    print("\nDigite um valor maior do que zero.")
                    continue
            except ValueError:
                print("\nDigite um valor válido")
                continue
            break
        if escolha == "sacar":
            conta.processar_transacao(Saque(valor))
        elif escolha == "depositar":
            conta.processar_transacao(Deposito(valor))

class Conta:
    def __init__(self, agencia:str, numero:str, saldo:float=0, cliente:Cliente=""):
        self.agencia = agencia
        self.__numero_conta = numero
        self.__saldo = saldo
        self.cliente = cliente
        self.__historico = Historico()


    @property
    def historico(self):
        return self.__historico
    @property
    def saldo(self):
        return self.__saldo
    @saldo.setter
    def saldo(self, novo_saldo):
        self.__saldo = novo_saldo
        if self.__saldo < 0:
            self.__saldo = 0
    @property
    def numero_conta(self):
        return self.__numero_conta
    
    def verificar_saldo(self):
        return f"R${self.saldo}".replace(".", ",")

    def processar_transacao(self, transacao):
       transacao.registrar(self)
            

    def exibir_extrato(self):
        while True:
            escolha = input("\nEscolha a forma de extrato: [extrato_do_dia] [extrato_geral] ").strip().lower()
            if not escolha or escolha not in ["extrato_do_dia", "extrato_geral"]:
                print("Digite algo válido")
                continue
            break
        if escolha == "extrato_geral":
            if len(self.historico.transacoes) == 0:
                print("\nNenhuma transação feita ainda.")
            print("\n" + "=" * 40)
            print("TRANSAÇÕES".center(40))
            print("=" * 40)
            for transacao in self.historico.transacoes:
                for k, v in transacao.items():
                    print(f"\n{k}:\t{v}")
                print("\n" + "=" * 40)
                print(f"R${self.saldo}".replace(".", ","))
                print("=" * 40)
        if escolha == "extrato_do_dia":
            if len(self.historico.transacoes) == 0:
                print("\nNenhuma transação feita ainda.")
            transacao_dia = self.historico.transacoes_hoje()
            print("\n" + "=" * 40)
            print("TRANSAÇÕES DO DIA".center(40))
            print("=" * 40)
            for transacao in transacao_dia:
                for k, v in transacao.items():
                    print(f"\n{k}:\t{v}")
                print("\n" + "=" * 40)
                print(f"R${self.saldo}".replace(".", ","))
                print("=" * 40)
        else:
            print("\nErro")
            return

class ContaCorrente(Conta):
    def __init__(self, agencia, numero, saldo = 0, cliente = "", limite_diario = 10):
        super().__init__(agencia, numero, saldo, cliente)
        self.__limite_diario = limite_diario

    @property
    def limite_diario(self):
        return self.__limite_diario
    
    @limite_diario.setter
    def limite_diario(self, limite_novo):
        if self.limite_diario <= 0:
            print("\nErro")
        else:
            self.__limite_diario = limite_novo

    def processar_transacao(self, transacao):
        if len(self.historico.transacoes) > 0:
            data_hoje = datetime.now().date()
            data_ultima_transacao = datetime.strptime(self.historico.transacoes[-1]['data'], "%Y/%m/%d")
            if data_hoje != data_ultima_transacao:
                self.__limite_diario = 10
        transacao.registrar(self)
        
class Transacao(ABC):

    @abstractmethod
    def registrar(self):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo < self.valor:
            print(f"\nA conta {conta.numero_conta}, não possui saldo o suficiente para conseguir sacar esse valor.")
            return
        if hasattr(conta, 'limite_diario'):
            if conta.limite_diario <= 0:
                print(f"\nA conta {conta.numero_conta} atingiu o seu limite de saques.")
                return
            conta.limite_diario -= 1
    
        conta.saldo -= self.valor        
        conta.historico.adicionar_transacao(self)
        print(f"\nSaque de R${self.valor:.2f} realizado com sucesso!".replace(".", ","))
                

class Historico:
    def __init__(self):
        self.__transacoes = []

    @property
    def transacoes(self):
        return self.__transacoes
    
    def adicionar_transacao(self, transacao:Transacao):
        self.__transacoes.append(
            {
                'tipo': transacao.__class__.__name__,
                'valor': f"R${transacao.valor:.2f}".replace(".", ","),
                'data': datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            }
        )

    def transacoes_hoje(self):
        transacoes_dia = []
        data_hoje = datetime.now().date()
        for transacao in self.__transacoes:
            transacao_f = datetime.strptime(transacao['data'], "%Y/%m/%d")
            if transacao_f == data_hoje:
                transacoes_dia.append(transacao)
        return transacoes_dia


def gerar_cliente():
        while True:
            cpf_cliente = input("\nDigite o seu cpf(apenas números): ").strip()
            if not cpf_cliente.isdecimal() or not cpf_cliente or len(cpf_cliente) > 11:
                print("\nDigite um cpf válido")
                continue
            break 
        while True:
            nome = input("\nDigite o seu nome: ").strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
            if not nome.replace(" ", "").isalpha():
                print("\nDigite apenas palavras nessa opção.")
                continue
            break
        while True:
            endereco = []
            endereco_local = input("\nDigite o seu endereço: ").strip().title().replace(" De ", " de ").replace(" Da ", " da ").replace(" Do ", " do ")
            if not endereco_local.replace(" ", "").isalpha():
                print("\nDigite apenas palavras nessa opção.")
                continue
            break
        endereco.append(endereco_local)
        while True:
            endereco_numero = input("\nDigite o número do seu endereço: ").strip()
            if not endereco_numero.isdecimal():
                print("\nDigite apenas números nessa opção")
                continue
            break
        endereco.append(endereco_numero)
        endereco = f"{endereco_local} {endereco_numero}"
        return Cliente(nome=nome, cpf=cpf_cliente, endereco=endereco)

def main():
    meu_banco = Banco("Banco Central Python")
    
    while True:
        print("\n" + "<" + ("=" * 40) + ">")
        print(f"{meu_banco.nome_banco.upper()}".center(40))
        print("<" + ("=" * 40) + ">")
        print("1 - Cadastrar novo Cliente")
        print("2 - Abrir nova Conta")
        print("3 - Acessar Conta (Saque, Depósito, Extrato)")
        print("4 - Listar todas as Contas")
        print("0 - Sair")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ").strip()

        match opcao:
            case "1":
                meu_banco.registrar_cliente()
            case "2":
                meu_banco.abrir_conta()
            case "3":
                meu_banco.solicitacao()
            case "4":
                meu_banco.listar_contas()
            case "0":
                print("\nSaindo do sistema bancário. Obrigrado por usar o nosso banco!")
                break
            case _:
                print("\nOpção inválida.")

main()