import os
import shutil
from pathlib import Path


#NOTE: o Path faz com que o arquivo que você está executando se torne um objeto, podendo manipular os arquivos e etc, e o .parent faz com que o arquivo recebido pelo Path retorne um arquivo pra cima 
ROOT_PATH = Path(__file__).parent

#NOTE: cria uma nova pasta(com o os.mkdir) na pasta atual do arquivo
#os.mkdir(ROOT_PATH / "meu-diretorio")

#NOTE: criando o arquivo dentro da pasta que estamos 
arquivo = open(ROOT_PATH / "novo.txt", 'w', encoding='utf-8')
arquivo.close()

#NOTE: você coloca o caminho da pasta aonde o arquivo está, o nome do arquivo, e após isso o caminho novamente do arquivo e o seu nome modificado(isso tudo com o os.rename)
#os.rename(ROOT_PATH / "novo.txt", ROOT_PATH / "modificando.txt")

#NOTE: você coloca o caminho da pasta aonde o arquivo está, e o nome do arquivo que você quer excluir
#os.remove(ROOT_PATH / "modificando.txt")

#NOTE: você coloca o caminho da pasta aonde o arquivo está, depois a localização do diretorio para aonde o arquivo será movido e o nome do arquivo 
shutil.move(ROOT_PATH / "novo.txt", ROOT_PATH / "meu-diretorio" / "novo.txt")
