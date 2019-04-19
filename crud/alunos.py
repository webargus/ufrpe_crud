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

#  Variáveis globais do módulo:
#
# nome do arquivo .csv para salvar o cadastro de alunos
arquivo = "alunos"
#
# lista com cópia do arquivo para as operações CRUD na memória
lista = []
#
# dicionário de formatação do cabeçalho de impressão da lista de alunos;
# as chaves são os nomes das colunas e os valores são as larguras das colunas
cabeçalho = {"CPF": "15", "Nome": "50"}
#


def _novo_aluno():
    while True:
        cpf = input("Entre o CPF do aluno (0 - aborta):\n")
        if cpf == "0":
            print("Operação abortada")
            return
        if f.validar_cpf(cpf):
            #   faz busca pelo CPF e nega inclusão se cadastro já existente
            cpf = f.formatar_cpf(cpf)
            indice = acha_cpf_aluno(cpf)
            if indice > -1:
                print("O aluno com o CPF %s já está cadastrado no sistema" % cpf)
            else:
                break
        else:
            print("CPF inválido (somente algarismos, 11 dígitos): tente novamente")

    while True:
        nome = input("Entre o nome do aluno (0 - aborta):\n")
        if nome == "0":
            print("Operação abortada")
            return
        nome = nome.strip()
        if len(nome) > 0:
            break
        else:
            print("Nome inválido: tente novamente")
    # Acrescenta aluno à lista e salva arquivo
    lista.append([cpf, nome])
    _salvar_cadastro()


def _alterar_cadastro():
    if len(lista) == 0:
        print("***Não há alunos cadastrados para alteração\n")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) do aluno cujo nome deseja alterar (0 - aborta):\n"))
            if ord > len(lista):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    print("CPF: %s" % (lista[ord][0]))
    print("Nome: %s" % (lista[ord][1]))
    nome = input("Entre o nome correto do aluno (Enter = mantem):\n")
    nome = nome.strip()
    if len(nome) > 0:
        lista[ord][1] = nome
        _salvar_cadastro()


def _excluir_aluno():
    if len(lista) == 0:
        print("***Não há alunos cadastrados para exclusão\n")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) do aluno que deseja excluir (0 - aborta):\n"))
            if ord > len(lista):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    print("CPF: %s" % (lista[ord][0]))
    print("Nome: %s" % (lista[ord][1]))
    #   TODO: Nega exclusão se aluno vinculado a alguma turma
    resp = input("Confirma a exclusão desse aluno?\n(sim = confirma): ")
    if resp.lower() != 'sim':
        return
    del lista[ord]
    _salvar_cadastro()


def _ler_cadastro():
    del lista[:]    # limpa lista antes de ler
    f.ler_arquivo(arquivo, lista)


def _salvar_cadastro():
    f.salvar_arquivo(arquivo, lista)


def acha_cpf_aluno(cpf):
    # Função para encontrar um CPF na lista;
    # retorna o índice do cadastro na lista se o CPF do aluno existir
    # ou -1 se o CPF não estiver cadastrado
    for indice, cadastro in enumerate(lista):
        if cadastro[0] == cpf:
            return indice
    return -1


def imprime_tabela():
    f.imprimir_tabela(cabeçalho, lista)


def alunos():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Cadastro de alunos".upper())
        imprime_tabela()
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


# As opções de menu estão numa lista de tuplas contendo o rótulo da opção
# e a função que deve ser executada mediante a escolha de uma opção;
# o objetivo é facilitar seja a exclusão de opções existentes
# ou a inclusão de novas opções, caso seja necessário modificar a rotina.
opções = [("Sair", lambda _=None: True), ("Novo aluno", _novo_aluno),
          ("Alterar cadastro", _alterar_cadastro),
          ("Excluir aluno", _excluir_aluno)]

#   inicializa o módulo lendo o cadastro do arquivo para a memória
_ler_cadastro()











