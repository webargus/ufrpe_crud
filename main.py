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

import sys
from crud.professores import professores
from crud.disciplinas import disciplinas
from crud.alunos import alunos
from crud.relatorios import relatorios
from crud.turmas import turmas


def sair():
    print("F I M")
    sys.exit(0)


# As opções de menu estão numa lista de tuplas contendo o rótulo da opção
# e a função que deve ser executada mediante a escolha de uma opção;
# o objetivo é facilitar seja a exclusão de opções existentes
# ou a inclusão de novas opções, caso seja necessário modificar o programa.
opções = [("Sair", sair), ("Professores", professores),
          ("Disciplinas", disciplinas), ("Alunos", alunos),
          ("Turmas", turmas), ("Relatórios", relatorios)]

# loop para entrada de opção de menu com bloco try-except para forçar
# o usuário a entrar uma opção válida:
while True:
    print("")
    print("**********   projeto crud - Sistema de controle acadêmico simplificado   **********".upper())
    s = "menu principal"
    print("\n\t\t" + s.upper())
    print("\t\t" + "-"*len(s))

    # imprime o número de cada opção e sua descrição:
    for opção, tupla in enumerate(opções):
        print("%d - %s" % (opção, tupla[0]))
    print("")

    try:
        opção = int(input("Entre o número da opção desejada: \n"))
        if opção < 0 or opção >= len(opções):
            raise ValueError
        rótulo = opções[opção][0]
        # aqui Python executa o bloco 'except' caso a opção digitada (var. opção)
        # não exista na lista de opções do menu (var. opções)
    except ValueError:
        print("Opção inválida :(")
        continue

    # chama a função que executa a opção desejada;
    # essas funções estão codificadas em módulos de mesmo nome
    # (ver os 'import' no topo)
    opções[opção][1]()



