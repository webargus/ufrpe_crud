"""
    *************************************************************************
    *                                                                       *
    *   Projeto CRUD / Sistema de Controle Acadêmico Simplificado           *
    *                                                                       *
    *   Autor: Edson Kropniczki - BSI - 2019.1 - Introdução â programação   *
    *   Professor: Gilberto Cysneiros Filho                                 *
    *                                                                       *
    *   Funções auxiliares compartilhadas pelo sistema CRUD                 *
    *                                                                       *
    *                                                                       *
    *************************************************************************
"""

import re
cpf_pattern = r"^\d{11}$"               # expressão regular para validar CPF
disciplina_pattern = r"^\d{5}$"         # expressão regular para validar código de disciplina
periodo_pattern = r"^\d{4}\.\d{1}$"     # expressão regular para validar período de turma


#   Funções para serialização de dados baseados em listas, que são salvas em arquivos no formato .csv,
#   prevendo eventual migração para base de dados no futuro.
#   Os campos de dados são salvos como strings entre aspas separadas
#   por ';' e terminadas por '\n' no formato
#   "campo 1";"campo 2"; ... "campo n"


def ler_arquivo(arquivo, lista):
    # parâmetros:
    # @arquivo  =   string com o nome do arquivo a ser lido
    # @lista    =   lista para salvar na mémoria os dados lidos
    # Lê as linhas do arquivo em formato .csv e as salva na lista (@lista), inserindo os
    # campos de dados conforme explicado na função salvar_arquivo (ver abaixo)
    try:
        # tenta abrir o arquivo se ele já existe
        handle = open(arquivo + ".csv", "r", encoding="utf-8")
    except OSError:
        # cria novo arquivo vazio se ele não existe
        handle = open(arquivo + ".csv", "w", encoding="utf-8")
        handle.close()
        return
    # copia linhas do arquivo para lista e retorna a lista
    for linha in handle.readlines():
        linha = linha.strip()   # remove /n do final da linha
        linha = linha[1:-1]     # remove aspas duplas do início e do final da linha
        # divide campos da linha separados por ";" e os adiciona à lista de retorno
        linha = linha.split('";"')
        linha = [_restaurar_separador(x) for x in linha]
        lista.append(linha)
    handle.close()      # fecha acesso ao arquivo


def salvar_arquivo(arquivo, *lista):
    # parâmetros:
    # @arquivo  =   string com o nome do arquivo para salvar dados
    # @lista    =   lista com os dados a serem salvos no arquivo;
    #               formato = matriz contendo m linhas X n colunas com os campos de dados a salvar:
    #               [[campo-0-0, campo-0-1, ..., campo-0-(n-1)],
    #                [campo-1-0, campo-1-1, ... campo-1-(n-1)],
    #                ...
    #                [campo-(m-1)-0, campo-(m-1)-1, ... campo-(m-1)-(n-1)]]
    try:
        handle = open(arquivo + ".csv", "w", encoding="utf-8")      # tenta abrir arquivo para escrita em formato UTF-8
    except OSError:
        print("Erro ao tentar abrir arquivo: %s" % (arquivo + '.csv'))  # informa ao usuário se houve erro
    else:
        for l in lista:         # lê linhas da lista para a variável @l
            for ll in l:        # lê lista contendo as colunas para a variável @ll
                #   salva as colunas separadas por aspas duplas + ponto-e-vírgula ('";"') e terminadas por new line (\n)
                handle.write(''.join(['"' + _escapar_separador(x) + '";' for x in ll])[:-1] + "\n")
        handle.close()  # fecha o acesso ao arquivo


def _escapar_separador(str):
    #   escapa campo de dados (parâmetro de entrada str) antes de salvá-lo em arquivo
    #   inserindo barra invertida (\) antes de eventual ponto-e-vírgula (;), se existir na cadeia de caracteres (str)
    return str.replace(';', '\;')


def _restaurar_separador(str):
    #   restaura sequência de escape de campo de dados lido de arquivo (parâmetro str),
    #   removendo barra invertida ('\') antes de ponto-e-vírgula, se houver
    return str.replace('\;', ';')


#   Funções para validação e formatação de dados

def validar_cpf(cpf):
    #   Função para validar CPF; retorna True se CPF válido, False se não válido
    if re.match(cpf_pattern, cpf) is None:
        return False
    return True


def formatar_cpf(cpf):
    #   retorna string de CPF no formato xxx.xxx.xxx-xx
    ret = ''        # string acumuladora do CPF formatado
    for x in range(0, 9, 3):        # acrescenta '.' a cada 3 algarismos
        ret += cpf[x:x+3] + '.'
    ret = ret[:-1]                  # descarta o último '.' acrescentado e
    ret += '-' + cpf[-2:]           # substitui por um '-' seguido dos 2 últimos algarismos
    return ret


def validar_disciplina(codigo):
    #   verifica se o código da disciplina consiste em string de 5 algarismos
    if re.match(disciplina_pattern, codigo) is None:
        return False
    return True


def validar_periodo(periodo):
    #   verifica se o periodo está no formato aaaa.s, p.ex., 2019.1, 2018.2
    if re.match(periodo_pattern, periodo) is None:
        return False
    return True


#   Função para copiar listas compostas
#   OBS: evitei importar o módulo copy para esse fim, por recomendação do projeto
def copiar_lista(lista):
    #   Lição aprendida:
    #   Quando se quer copiar uma lista composta, do tipo lista1 = [[1, 2, 3],[4, 5, 6],...[x, y, z]], por exemplo,
    #   nenhuma das opções abaixo funciona:
    #
    #   lista2 = lista1.copy()      #   falha
    #
    #   lista2 = lista1[:]          #   falha
    #
    #   lista2 = []
    #   for x in lista1:            #   falha
    #       lista2.append(x)
    #
    #   Explicação:
    #   Todas as alternativas acima fazem meramente uma cópia rasa (shallow copy) da lista, na qual
    #   Python mantem as referências internas de memória para as sub-listas da lista composta inalteradas.
    #   A consequência é que, ao fazer qualquer modificação na 'cópia' (lista2), essa alteração também ocorre
    #   na lista original (lista1).
    #   Na prática, o método copy() NÃO FUNCIONA, quando se trata de listas compostas
    #   A solução é criar uma nova lista copiando as listas internas uma por uma, usando compreensão de listas:
    return [[x for x in y] for y in lista]


#   Função para impressão de tabelas de relatórios na tela
def imprimir_tabela(headers, dados):

    #   Imprime dados formatados em tabela
    #
    #   Entradas:
    #       Cabeçalho: headers = {"nome campo 0": "tamanho", ..., "nome campo n-1": "tamanho"}
    #       Dados a imprimir: matriz m linhas X n colunas
    #       dados = [[dado 0, ... dado n-1], ..., [dado 0, ... dado n-1]]
    #
    #   +----+------------+-------------+--------+-------------+
    #   |ORD |campo-0     |campo-1      |  ...   |campo-(n-1)  |
    #   +----+------------+-------------+--------+-------------+
    #   | 1  |dado[0][0]  |dado[0][1]   |  ...   |dado[0][n-1] |
    #   +----+------------+-------------+--------+-------------+
    #                           ...
    #   +----+------------+-------------+--------+-------------+
    #   | m  |dado[m-1][0]|dado[m-1][1] |  ...   |dado[m-1][n-1]   |
    #   +----+------------+-------------+--------+-------------+
    #

    #   copia strings das larguras de cada coluna (cabeçalho) da tabela
    lars = list(headers.values())
    larguras = [int(l) for l in lars]   # faz cast das larguras das colunas para int
    larguras.insert(0, 4)               # insere a largura da coluna padrão ORD
    # constrói borda superior/inferior da tabela
    borda = ''
    for largura in larguras:
        borda += '+' + "-"*(largura)
    borda += '+'
    print(borda)    # imprime borda superior
    print('|' + '{:^4}'.format('ORD'), end='')      # imprime coluna padrão ORD
    for header, largura in headers.items():         # imprime cabeçalho conforme formatado no parâmetro @headers3
        formato = '{:' + largura + '}'
        print('|' + formato.format(header.upper()), end='')
    print('|')
    print(borda)
    for linha in range(len(dados)):
        print('|' + '{:^4}'.format(str(linha + 1)), end='')
        for coluna in range(len(dados[linha])):
            formato = '{:' + lars[coluna] + '}'
            print('|' + formato.format(dados[linha][coluna]), end='')
        print('|')
        print(borda)
















