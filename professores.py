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

import ferramentas

arquivo = "professores"


def novo_cadastro():
    return


def buscar_cadastro():
    return


def menu_professores():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("")
        s = "Cadastro de Professores"
        print("\n\t\t" + s.upper())
        print("\t\t" + "-" * len(s))
        # As opções de menu estão numa lista de tuplas contendo o rótulo da opção
        # e a função que deve ser executada mediante a escolha de uma opção;
        # o objetivo é facilitar seja a exclusão de opções existentes
        # ou a inclusão de novas opções, caso seja necessário modificar a rotina.
        opções = [("Voltar", lambda _ : True), ("Novo cadastro", novo_cadastro),
                  ("Busca", buscar_cadastro)]
        # imprime o número de cada opção e sua descrição:
        for opção, tupla in enumerate(opções):
            print("%d - %s" % (opção, tupla[0]))
        print("")

        try:
            opção = int(input("Entre o número da opção desejada: "))
            # aqui Python executa o bloco 'except' caso a opção digitada (var. opção)
            # não exista na lista de opções do menu (var. opções):
            rótulo = opções[opção][0]
        except Exception:
            print("Opção inválida")
            continue

        # chama a função que executa a opção desejada;
        opções[opção][1](None)


def professores():
    menu_professores()

    return








