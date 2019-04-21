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
# nome do arquivo .csv para salvar o cadastro de disciplinas
arquivo = "disciplinas"
#
# lista com cópia do arquivo para as operações CRUD na memória
lista = []
#
# dicionário de formatação do cabeçalho de impressão da lista de disciplinas;
# as chaves são os nomes das colunas e os valores são as larguras das colunas
cabeçalho = {"Código": "15", "Nome": "40"}
#


def _nova_disciplina():
    while True:
        codigo = input("Entre o código da disciplina (0 - aborta):\n")
        if codigo == "0":
            print("Operação abortada")
            return
        if f.validar_disciplina(codigo):
            #   faz busca pelo código e nega inclusão se cadastro já existente
            disc = acha_disciplina(codigo)
            if disc is not None:
                print("A disciplina %s - '%s' já está cadastrada no sistema" % disc)
            else:
                break
        else:
            print("Código inválido (somente algarismos, 5 dígitos): tente novamente")

    while True:
        nome = input("Entre o nome da disciplina (0 - aborta):\n")
        if nome == "0":
            print("Operação abortada")
            return
        nome = nome.strip()
        if len(nome) > 0:
            break
        else:
            print("Nome inválido: tente novamente")
    # Acrescenta nova disciplina à lista e salva arquivo
    lista.append([codigo, nome])
    _salvar_cadastro()


def _alterar_disciplina():
    if len(lista) == 0:
        print("***Não há disciplinas cadastradas para alteração\n")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) da disciplina cujo nome deseja alterar (0 - aborta):\n"))
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
    print("Código: %s" % (lista[ord][0]))
    print("Nome: %s" % (lista[ord][1]))
    nome = input("Entre o nome correto da disciplina (Enter = mantem):\n")
    nome = nome.strip()
    if len(nome) > 0:
        lista[ord][1] = nome
        _salvar_cadastro()


def _excluir_disciplina():
    if len(lista) == 0:
        print("***Não há disciplinas cadastradas para exclusão\n")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) da disciplina que deseja excluir (0 - aborta):\n"))
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
    print("Código: %s" % (lista[ord][0]))
    print("Nome: %s" % (lista[ord][1]))
    #   TODO: Nega exclusão se disciplina vinculada a alguma turma
    resp = input("Confirma a exclusão dessa disciplina?\n(sim = confirma): ")
    if resp.lower() != 'sim':
        return
    del lista[ord]
    _salvar_cadastro()


def _ler_cadastro():
    del lista[:]    # limpa lista antes de ler
    f.ler_arquivo(arquivo, lista)
    lista.sort(key=lambda disciplina: disciplina[1].lower())


def _salvar_cadastro():
    f.salvar_arquivo(arquivo, lista)


def acha_disciplina(codigo):
    # Função para encontrar uma disciplina na lista pelo código da disciplina;
    # retorna tupla do cadastro na lista se existir o código
    # ou None se o código não estiver cadastrado
    for cadastro in lista:
        if cadastro[0] == codigo:
            return cadastro.copy()
    return None


def exportar_tabela():
    f.imprimir_tabela(cabeçalho, lista)
    return f.copiar_lista(lista)


def disciplinas():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Cadastro de disciplinas".upper())
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


# As opções de menu estão numa lista de tuplas contendo o rótulo da opção
# e a função que deve ser executada mediante a escolha de uma opção;
# o objetivo é facilitar seja a exclusão de opções existentes
# ou a inclusão de novas opções, caso seja necessário modificar a rotina.
opções = [("Sair", lambda _=None: True), ("Nova disciplina", _nova_disciplina),
          ("Alterar disciplina", _alterar_disciplina),
          ("Excluir disciplina", _excluir_disciplina)]

#   inicializa o módulo lendo o cadastro do arquivo para a memória
_ler_cadastro()





