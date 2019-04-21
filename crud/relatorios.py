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

import datetime
import crud.ferramentas as f
from crud.turmas import _imprimir_turmas
from crud.turmas import _exportar_turmas as importar_turmas
from crud.turmas import _exportar_professores as importar_professores
from crud.turmas import _exportar_alunos as importar_alunos
from crud.professores import acha_professor
from crud.disciplinas import acha_disciplina
from crud.alunos import acha_aluno

lista_turmas = []
lista_profs = []
lista_alunos = []

cabeçalho_ata = {"Nota": "6", "CPF": "15", "Nome do(a) aluno(a)": "50", "Assinatura": "40"}


def _imprimir_ata():
    _imprimir_turmas()
    while True:
        try:
            ord = int(input("Entre o número (ORD) da turma para impressão de ata (0 - aborta):\n"))
            if ord < 0 or ord > len(lista_turmas):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    id_turma = lista_turmas[ord][0]
    codigo = lista_turmas[ord][3]
    lista = [x for aluno in lista_alunos if aluno[0] == id_turma for x in [acha_aluno(aluno[1])]]
    if len(lista) == 0:
        print("Não há alunos inscritos nessa turma, nada a listar.")
        return
    for x in lista:
        x.insert(0, '')
        x.append('')
    lista.sort(key=lambda aluno: aluno[2])
    larguras = cabeçalho_ata.values()
    largura = sum([int(x) for x in larguras]) + 2*(len(larguras) + 1)
    print("="*largura)
    print()
    print(('{:^' + str(largura) + '}').format("universidade federal rural de pernambuco".upper()))
    print(('{:^' + str(largura) + '}').format('Ata de Exercício'))
    agora = datetime.datetime.now()
    print()
    print(('{:^' + str(largura) + '}').format(agora.strftime("%d/%m/%y - %H:%M")))
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    print("Código da disciplina: %s" % codigo)
    print("Nome da Disciplina: %s" % (acha_disciplina(codigo)[1]))
    print("Professor(es): %s" % (', '.join([acha_professor(x[1])[1] for x in lista_profs if x[0] == id_turma])))
    print()
    f.imprimir_tabela(cabeçalho_ata, lista)
    print()
    print("="*largura)


def _turmas_por_professor():
    pass


def _disciplinas_por_aluno():
    pass


def _inicializa():
    global lista_turmas
    lista_turmas = importar_turmas()
    global lista_profs
    lista_profs = importar_professores()
    global lista_alunos
    lista_alunos = importar_alunos()


def relatorios():
    _inicializa()
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Relatórios".upper())
        # imprime o número de cada opção e sua descrição:
        for opção, tupla in enumerate(opções):
            print("%d - %s" % (opção, tupla[0]))
        print("")

        try:
            opção = int(input("Entre o número da opção desejada: \n"))
            if opção < 0 or opção >= len(opções):
                raise ValueError
            print("Opção: %s" % (opções[opção][0]))
            # aqui Python executa o bloco 'except' caso a opção digitada (var. opção)
            # não exista na lista de opções do menu (var. opções):
        except ValueError:
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
opções = [("Sair", lambda _=None: True),
          ("Ata de exercício", _imprimir_ata),
          ("Turmas por professor", _turmas_por_professor),
          ("Disciplinas por aluno", _disciplinas_por_aluno)]

_inicializa()


