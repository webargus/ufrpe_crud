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

import crud.ferramentas as f

#  Variáveis do módulo:
arquivo = "professores"  # nome do arquivo .csv para salvar o cadastro de professores
lista = []               # lista com cópia do arquivo para as operações CRUD na memória
# dicionário de formatação do cabeçalho de impressão da lista de professores cadastrados;
# as chaves são os nomes das colunas e os valores são as larguras das colunas
cabeçalho = {"CPF": "15", "Nome": "50", "Departamento": "18"}


def _novo_cadastro():
    while True:
        cpf = input("Entre o CPF do professor (0 - aborta):\n")
        if cpf == "0":
            print("Operação abortada")
            return
        if f.validar_cpf(cpf):
            #   faz busca pelo CPF e nega inclusão se cadastro já existente
            cpf = f.formatar_cpf(cpf)
            indice = acha_cpf(cpf)
            if indice > -1:
                print("O CPF %s já está cadastrado no sistema" % cpf)
            else:
                break
        else:
            print("CPF inválido (somente algarismos, 11 dígitos): tente novamente")

    while True:
        nome = input("Entre o nome do professor (0 - aborta):\n")
        if nome == "0":
            print("Operação abortada")
            return
        nome = nome.strip()
        if len(nome) > 0:
            break
        else:
            print("Nome inválido: tente novamente")

    while True:
        depto = input("Entre o departamento do professor (0 - aborta):\n")
        if depto == "0":
            print("Operação abortada")
            return
        depto = depto.strip()
        if len(depto) > 0:
            break
        else:
            print("Departamento inválido: tente novamente")

    #   print("CPF: %s; Nome: %s; Depto: %s" % (cpf, nome, depto))  #   debug
    #   inclui cadastro na lista
    lista.append([cpf, nome, depto])
    _salvar_cadastro()


def _alterar_cadastro():
    while True:
        try:
            ord = int(input("Entre o número (ORD) do professor cujos dados deseja alterar (0 - aborta):\n"))
            if ord > len(lista):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    print("CPF: %s" % (lista[ord-1][0]))
    print("Nome: %s" % (lista[ord-1][1]))
    print("Departamento: %s" % (lista[ord-1][2]))
    salvar = False
    nome = input("Entre o nome correto do professor (Enter = mantem):\n")
    nome = nome.strip()
    if len(nome) > 0:
        lista[ord-1][1] = nome
        salvar = True
    depto = input("Entre o departamento do professor (Enter = mantem):\n")
    depto = depto.strip()
    if len(depto) > 0:
        lista[ord-1][2] = depto
        salvar = True
    if salvar:
        _salvar_cadastro()

def _ler_cadastro():
    del lista[:]    # limpa lista antes de ler
    f.ler_arquivo(arquivo, lista)


def _salvar_cadastro():
    f.salvar_arquivo(arquivo, lista)


def _menu_professores():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Cadastro de Professores".upper())
        f.imprimir_tabela(cabeçalho, lista)
        # imprime o número de cada opção e sua descrição:
        for opção, tupla in enumerate(opções):
            print("%d - %s" % (opção, tupla[0]))
        print("")

        try:
            opção = int(input("Entre o número da opção desejada: \n"))
            # aqui Python executa o bloco 'except' caso a opção digitada (var. opção)
            # não exista na lista de opções do menu (var. opções):
            print("Opção: %s" % (opções[opção][0]))
        except Exception:
            print("Opção inválida :(")
            continue

        # chama a função que executa a opção desejada;
        opções[opção][1]()
        if opção == 0:
            break  # retorna para o menu principal


def acha_cpf(cpf):
    for indice, cadastro in enumerate(lista):
        if cadastro[0] == cpf:
            return indice
    return -1


def professores():
    _menu_professores()


# As opções de menu estão numa lista de tuplas contendo o rótulo da opção
# e a função que deve ser executada mediante a escolha de uma opção;
# o objetivo é facilitar seja a exclusão de opções existentes
# ou a inclusão de novas opções, caso seja necessário modificar a rotina.
opções = [("Sair", lambda _=None: True), ("Novo cadastro", _novo_cadastro),
          ("Alterar cadastro", _alterar_cadastro)]

#   inicializa o módulo lendo o cadastro para a memória
_ler_cadastro()







