
#NOTE: Se você usar o modo de escrita, o nome do arquivo pode ser substituido para gerar um novo, mas apenas no modo de escrita
arquivo = open('C:/Users/DVTI/Documents/ESTUDOS - PL/logica_com_python/dio/teste.txt', 'w')

#NOTE: escreve liha a linha de um arquivo gerado
arquivo.write("Escrevendo dados em um novo arquivo.")

#NOTE: recebe um valor interavél do tipo str, lendo cada valor da lista/objeto/tupla e juntando toda a palavra no final(como um "".join())
arquivo.writelines("Python")
arquivo.close()
