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
from crud.disciplinas import exportar_tabela as importar_disciplinas
from crud.professores import acha_professor
from crud.professores import exportar_tabela as importar_professores

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
        disciplinas = importar_disciplinas()
        if len(disciplinas) == 0:
            print("***Não há disciplinas cadastradas")
            print("\tNo menu principal, escolha a opção '2 - disciplinas->1 - Nova disciplina' e cadastre a disciplina\n")
            return
        while True:
            try:
                ord = int(input("Entre o número (ORD) da disciplina (0 - aborta):\n"))
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

    #   inclui turma na memória e a salva em arquivo
    lista_turmas.append([id_turma, codigo, periodo, disciplinas[ord][0]])
    _salvar_turmas()

"""
def _alterar_turma():
    if len(lista_turmas) == 0:
        print("Não há turmas cadastradas, nada a alterar...")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) da turma que deseja alterar (0 - aborta):\n"))
            if ord > len(lista_turmas):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    print("Código da disciplina: %s" % (lista_turmas[ord][3]))
    _criar_turma(ord)
"""


def _excluir_turma():
    if len(lista_turmas) == 0:
        print("Cadastro de turmas vazio, não há turmas para excluir.")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) da turma que deseja excluir (0 - aborta):\n"))
            if ord > len(lista_turmas):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    print("Código da disciplina: %s" % (lista_turmas[ord][3]))
    print("ATENÇÃO! A exclusão dessa turma implica na exclusão de todos os professores e alunos a ela vinculados.")
    print("Confirma a exclusão dessa turma assim mesmo?")
    resp = input("(sim = confirma): ")
    if resp.lower() != 'sim':
        return
    id_turma = lista_turmas[ord][0]
    _elimina_professores(id_turma)
    _elimina_alunos(id_turma)
    del lista_turmas[ord]
    _salvar_turmas()
    _salvar_professores()
    _salvar_alunos()


def _incluir_professor():
    if len(lista_turmas) == 0:
        print("Não há turmas cadastradas para incluir professor")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) da turma para incluir professor (0 - aborta):\n"))
            if ord > len(lista_turmas):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    print("Código da disciplina: %s" % (lista_turmas[ord][3]))
    id_turma = lista_turmas[ord][0]

    # busca professor
    professores = importar_professores()
    if len(professores) == 0:
        print("***Não há professores cadastrados")
        print("\tNo menu principal, escolha a opção '1 - professores -> 1 - Novo cadastro' e cadastre professor\n")
        return
    while True:
        try:
            ord = int(input("Entre o número (ORD) do professor (0 - aborta):\n"))
            if ord > len(professores):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break

    ord -= 1
    cpf = professores[ord][0]
    print("CPF: %s" % cpf)
    print("Nome: %s" % (professores[ord][1]))
    profs = _acha_professores(id_turma)
    for prof in profs:
        if prof[0] == cpf:
            print("Esse professor já está a cargo dessa turma.")
            return
    lista_profs.append([id_turma, cpf])
    _salvar_professores()


def _excluir_professor():
    while True:
        try:
            ord = int(input("Entre o número (ORD) da turma do professor (0 - aborta):\n"))
            if ord > len(lista_turmas):
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
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    print("Código da disciplina: %s" % (lista_turmas[ord][3]))
    #   busca por professores da turma pela id da turma
    professores = _acha_professores(lista_turmas[ord][0])
    if len(professores) == 0:
        print("Não há professores designados para essa turma.")
        return
    pos = 0
    if len(professores) > 1:
        print("Professores:")
        for indice in range(len(professores)):
            print("\t%d - %s" % (indice + 1, professores[indice][1]))
        while True:
            try:
                pos = int(input("Remover qual professor (de 1 a %d):" % (len(professores))))
                if 1 > pos > len(professores):
                    raise ValueError
                else:
                    pos -= 1
                    break
            except ValueError:
                print("Entrada inválida :(")
    print("Remover professor: %s" % (professores[pos][1]))
    resp = input("Confirma a remoção (sim - remove)?")
    if resp.lower() != 'sim':
        return
    _remover_professor(id_turma, professores[pos][0])


def _remover_professor(id_turma, cpf):
    for entrada in lista_profs:
        if entrada[0] == id_turma and entrada[1] == cpf:
            lista_profs.remove(entrada)
            _salvar_professores()
            break


def _elimina_professores(id_turma):
    for entrada in lista_profs:
        if entrada[0] == id_turma:
            lista_profs.remove(entrada)
            _elimina_professores(id_turma)


def _elimina_alunos(id_turma):
    for entrada in lista_alunos:
        if entrada[0] == id_turma:
            lista_alunos.remove(entrada)
            _elimina_alunos(id_turma)


def _ler_turmas():
    del lista_turmas[:]    # limpa lista antes de ler
    f.ler_arquivo(turmas_geral, lista_turmas)


def _salvar_turmas():
    f.salvar_arquivo(turmas_geral, lista_turmas)


def _ler_professores():
    del lista_profs[:]
    f.ler_arquivo(turmas_profs, lista_profs)


def _salvar_professores():
    f.salvar_arquivo(turmas_profs, lista_profs)


def _ler_alunos():
    del lista_alunos[:]
    f.ler_arquivo(turmas_alunos, lista_alunos)


def _salvar_alunos():
    f.salvar_arquivo(turmas_alunos, lista_alunos)


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
            prof = acha_professor(entrada[1])
            if prof is not None:
                professores.append(prof)
    return professores


def _imprimir_turmas():
    # copia a lista de turmas
    lista = f.copiar_lista(lista_turmas)

    # prepara a cópia da lista de turmas para impressão
    for turma in lista:
        # inclui nome da disciplina na cópia
        # a posição 3 contém o código da disciplina na lista das turmas;
        # a posição 1 da lista retornada pela busca contém o nome da disciplina
        turma.append(acha_disciplina(turma[3])[1])
        # inclui o(s) nome(s) do(s) professor(es) na listagem
        # lista os nomes dos professores (conteúdos na posição 1) dos resultados da busca pelos professores
        # e une-os com vírgula
        professores = ', '.join([x[1] for x in _acha_professores(turma[0])])
        turma.append(professores)
    #  elimina campo da id da turma antes de imprimir
    lista = [x[1:] for x in lista]
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
          ("Excluir turma", _excluir_turma),
          ("Incluir professor", _incluir_professor),
          ("Excluir professor", _excluir_professor)]

#   inicializa o módulo lendo os cadastros de turmas do arquivo para a memória
_ler_alunos()
_ler_professores()
_ler_turmas()




















