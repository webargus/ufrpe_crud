"""
    *************************************************************************
    *                                                                       *
    *   Projeto CRUD / Sistema de Controle Acadêmico Simplificado           *
    *                                                                       *
    *   Autor: Edson Kropniczki - BSI - 2019.1 - Introdução â programação   *
    *   Professor: Gilberto Cysneiros Filho                                 *
    *                                                                       *
    *************************************************************************
"""

#   Ferramentas para ler/escrever em arquivos no formato .csv,
#   prevendo eventual migração para base de dados no futuro.
#   Os campos de dados são salvos como strings entre aspas separadas
#   por ';' e terminadas por '\n' no formato
#   "campo 1";"campo 2"; ... "campo n"


def ler_arquivo(arquivo):
    # retorna lista contendo as linhas de arquivo em formato .csv dispostas em listas
    # contendo os campos de dados de cada linha
    lista = []
    try:
        # tenta abrir o arquivo se ele já existe
        handle = open(arquivo + ".csv", "r", encoding="utf-8")
    except IOError:
        # cria novo arquivo vazio se ele não existe
        handle = open(arquivo + ".csv", "w", encoding="utf-8")
        handle.close()
        return lista
    # copia linhas do arquivo para lista e retorna a lista
    for linha in handle.readlines():
        linha = linha.strip()   # remove /n do final da linha
        linha = linha[1:-1]     # remove aspas duplas do início e do final da linha
        # pega campos da linha separados por ";" e os adiciona à lista de retorno
        linha = linha.split('";"')
        linha = [restaurar_aspas(x) for x in linha]
        lista.append(linha)
    handle.close()
    return lista


def salvar_arquivo(arquivo, *lista):
    handle = open(arquivo + ".csv", "w", encoding="utf-8")
    for l in lista:
        for ll in l:
            handle.write(''.join(['"' + escapar_aspas(x) + '";' for x in ll])[:-1] + "\n")
    handle.close()

def escapar_aspas(str):
    return str.replace(';', '\;')


def restaurar_aspas(str):
    return str.replace('\;', ';')




