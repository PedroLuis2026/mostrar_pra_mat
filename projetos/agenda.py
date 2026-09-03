from modulo_agenda import *
from datetime import *
print("Agenda".center(40, "="))





while True:
    info = carregar_info()
    escolha = input("\nAperte zero para verificar agenda, um para marcar outro compromisso, ou clique qualquer outro botão para sair: ")
    if escolha == "0":
        if info:
            for data, compromisso in info.items():
                print("=" * 40)
                print(f"\n{data}:\t{compromisso}")
                print("=" * 40)
                continue
        else:
            print("\nNenhum compromisso foi marcado ainda.")
            continue

    elif escolha == "1":
        print("=" * 40)
        nova_data = datetime.now().strftime("%Y/%m/%d")
        novo_compromisso = input("\nDigite o seu novo compromisso: ")
        salvar_info(nova_data, novo_compromisso)

    else:
        print("\nTá bom, até mais!")
        break

            
                

