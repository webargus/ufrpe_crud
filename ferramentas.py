"""
    *************************************************************************
    *                                                                       *
    *   Projeto CRUD / Sistema de Controle Acadêmico Simplificado           *
    *                                                                       *
    *   Autor: Edson Kropniczki - BSI - 2019.1 - Introdução â programação   *
    *   Professor: Gilberto Cysneiros Filho                                 *
    *                                                                       *
    *   Funções auxiliares compartilhadas pelo sistema                      *
    *                                                                       *
    *                                                                       *
    *************************************************************************
"""

import re
pattern = r"^\d{11}$"

#   Funções para ler/escrever em arquivos no formato .csv,
#   prevendo eventual migração para base de dados no futuro.
#   Os campos de dados são salvos como strings entre aspas separadas
#   por ';' e terminadas por '\n' no formato
#   "campo 1";"campo 2"; ... "campo n"


def ler_arquivo(arquivo, lista):
    # adiciona as linhas do arquivo em formato .csv dispostas em listas
    # contendo os campos de dados de cada linha
    try:
        # tenta abrir o arquivo se ele já existe
        handle = open(arquivo + ".csv", "r", encoding="utf-8")
    except IOError:
        # cria novo arquivo vazio se ele não existe
        handle = open(arquivo + ".csv", "w", encoding="utf-8")
        handle.close()
        return
    # copia linhas do arquivo para lista e retorna a lista
    for linha in handle.readlines():
        linha = linha.strip()   # remove /n do final da linha
        linha = linha[1:-1]     # remove aspas duplas do início e do final da linha
        # pega campos da linha separados por ";" e os adiciona à lista de retorno
        linha = linha.split('";"')
        linha = [_restaurar_separador(x) for x in linha]
        lista.append(linha)
    handle.close()


def salvar_arquivo(arquivo, *lista):
    handle = open(arquivo + ".csv", "w", encoding="utf-8")
    for l in lista:
        for ll in l:
            handle.write(''.join(['"' + _escapar_separador(x) + '";' for x in ll])[:-1] + "\n")
    handle.close()

def _escapar_separador(str):
    return str.replace(';', '\;')


def _restaurar_separador(str):
    return str.replace('\;', ';')


def validar_CPF(cpf):
    #   Função para validar CPF; retorna True se CPF válido, False se não válido
    if re.match(pattern, cpf) is None:
        return False
    return True


