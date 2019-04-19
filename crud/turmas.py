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
from crud.disciplinas import acha_disciplina
from crud.disciplinas import exportar_tabela as importar_tabela
from crud.professores import acha_professor

#  Variáveis globais do módulo:
#
# nome do arquivo .csv para salvar as turmas
turmas_geral = "turmas"
# nome do arquivo .csv para salvar os professores das turmas
turmas_profs = "turmas_professores"
# nome do arquivo .csv para salvar os alunos das turmas
turmas_alunos = "turmas_alunos"
#
# lista com cópia do arquivo para as operações CRUD com as turmas na memória
lista_turmas = []
# lista com cópia do arquivo para as operações CRUD com os professores das turmas
lista_profs = []
# lista com cópia do arquivo para as operações CRUD com os alunos das turmas
lista_alunos = []
#
# dicionário de formatação do cabeçalho de impressão da lista de turmas;
# as chaves são os nomes das colunas e os valores são as larguras das colunas
cabeçalho_turmas = {"Turma": "7", "Período": "8", "Código": "8", "Disciplina": "30", "Professor(es)": "50"}
#


def _criar_turma():
    while True:
        while True:
            codigo = input("Entre o código da turma (Enter - aborta):\n")
            codigo = codigo.strip()
            if len(codigo) == 0:
                print("Operação abortada")
                return
            if len(codigo) < 5:
                    # converte codigo para maiúsculas, para evitar entradas
                    # em duplicidade:
                    codigo = codigo.upper()
                    break
            else:
                print("Código inválido (4 caracteres no máximo): tente novamente")

        while True:
            periodo = input("Entre o período da turma (Enter - aborta):\n")
            periodo = periodo.strip()
            if len(periodo) == 0:
                print("Operação abortada")
                return
            if f.validar_periodo(periodo):
                break
            else:
                print("Período inválido (formato = aaaa.s, ex., 2019.1, 2018.2)")

        # pega disciplina
        disciplinas = importar_tabela()
        if len(disciplinas) == 0:
            print("***Não há disciplinas cadastradas para inclusão")
            print("\tNo menu principal, escolha a opção '2 - disciplinas->1 - Nova disciplina' e cadastre a disciplina\n")
            return
        while True:
            try:
                ord = int(input("Entre o número (ORD) da disciplina que deseja incluir (0 - aborta):\n"))
                if ord > len(disciplinas):
                    raise ValueError
            except ValueError:
                print("Entrada inválida :( tente novamente...")
                continue
            if ord == 0:
                print("Operação abortada")
                return
            break

        ord -= 1
        print("Código: %s" % (disciplinas[ord][0]))
        print("Nome: %s" % (disciplinas[ord][1]))
        id_turma = codigo + periodo + disciplinas[ord][0]
        turma = _acha_turma(id_turma)
        if turma is None:
            break
        else:
            print("Turma já cadastrada")
    #   inclui turma e salva arquivo
    lista_turmas.append([id_turma, codigo, periodo, disciplinas[ord][0]])
    _salvar_turmas()


def _alterar_turma():
    pass


def _excluir_turma():
    pass


def _ler_turmas():
    del lista_turmas[:]    # limpa lista antes de ler
    print(turmas_geral)
    f.ler_arquivo(turmas_geral, lista_turmas)


def _salvar_turmas():
    f.salvar_arquivo(turmas_geral, lista_turmas)


def _acha_turma(id_turma):
    # busca turma por id da turma e retorna tupla com dados da turma
    # ou None se turma não encontrada
    for turma in lista_turmas:
        if turma[0] == id_turma:
            return turma
    return None


def _acha_professores(id_turma):
    professores = []
    for entrada in lista_profs:
        if entrada[0] == id_turma:
            professores.append(acha_professor(entrada[1]))
    return professores


def _imprimir_turmas():
    lista = [x[1:] for x in lista_turmas.copy()]
    for turma in lista:
        turma.append(acha_disciplina(turma[2])[1])
        professores = _acha_professores(turma[0])
        turma.append('\n'.join([x[1] for x in professores]))
    f.imprimir_tabela(cabeçalho_turmas, lista)


def turmas():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Turmas".upper())
        _imprimir_turmas()
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
opções = [("Sair", lambda _=None: True),
          ("Criar turma", _criar_turma),
          ("Alterar turma", _alterar_turma),
          ("Excluir turma", _excluir_turma)]

#   inicializa o módulo lendo o cadastro de turmas do arquivo para a memória
_ler_turmas()




















