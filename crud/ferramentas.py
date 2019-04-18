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


def validar_cpf(cpf):
    #   Função para validar CPF; retorna True se CPF válido, False se não válido
    if re.match(pattern, cpf) is None:
        return False
    return True

def formatar_cpf(cpf):
    #   retorna string de CPF no formato xxx.xxx.xxx-xx
    ret = ''        # string acumuladora do retorno formatado
    for x in range(0, 9, 3):        # acrescenta '.' a cada 3 algarismos
        ret += cpf[x:x+3] + '.'
    ret = ret[:-1]                  # descarta o último '.' acrescentado e
    ret += '-' + cpf[-2:]           # substitui por um '-' seguido dos 2 últimos algarismos
    return ret


def imprimir_tabela(headers, dados):

    #   Imprime dados formatados em tabela
    #
    #   Entradas:
    #       Cabeçalho: headers = {"nome campo 0": tamanho, ..., "nome campo n-1": tamanho}
    #       Dados a imprimir: matriz m linhas X n colunas
#               dados = [[dado 0, ... dado n-1], ..., [dado 0, ... dado n-1]]
    #
    #   +------------+-------------+--------+-------------+
    #   |campo-0     |campo-1      |  ...   |campo-(n-1)  |
    #   +------------+-------------+--------+-------------+
    #   |dado[0][0]  |dado[0][1]   |  ...   |dado[0][n-1] |
    #   +------------+-------------+--------+-------------+
    #                           ...
    #   +------------+-------------+--------+-------------+
    #   |dado[m-1][0]|dado[m-1][1] |  ...   |dado[m-1][n-1]   |
    #   +------------+-------------+--------+-------------+
    #

    lars = list(headers.values())
    largura_total = sum([int(l) for l in lars])
    print("="*largura_total)
    print('{:^4}'.format('ORD'), end='')
    for header, largura in headers.items():
        formato = '{:' + largura + '}'
        print(formato.format(header), end='')
    print('')
    print("-"*largura_total)
    for linha in range(len(dados)):
        print('{:^4}'.format(str(linha + 1)), end='')
        for coluna in range(len(dados[linha])):
            formato = '{:' + lars[coluna] + '}'
            print(formato.format(dados[linha][coluna]), end='')
        print('')
    print("="*largura_total)
















