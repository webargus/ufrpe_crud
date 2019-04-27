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
            aluno = acha_aluno(cpf)
            if aluno is not None:
                print("O aluno com o CPF %s - %s já está cadastrado no sistema" % (aluno[0], aluno[1]))
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
    if len(lista) == 0:     #   aborta se lista de alunos vazia
        print("***Não há alunos cadastrados para alteração\n")
        return
    while True:
        try:
            #   entra número de ordem do aluno, conforme printado na lista de alunos mostrada na tela
            ord = int(input("Entre o número (ORD) do aluno cujo nome deseja alterar (0 - aborta):\n"))
            if ord < 0 or ord > len(lista):
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
        lista[ord][1] = nome        #   atualiza nome na memória
        _salvar_cadastro()          #   salva cadastro


def _excluir_aluno():
    if len(lista) == 0:     #   exibe mensagem informativa e retorna, caso a lista de alunos esteja vazia
        print("***Não há alunos cadastrados para exclusão\n")
        return
    while True:
        try:
            #   entra número de ordem do aluno a excluir, conforme printado na tabela de alunos mostrada na tela
            ord = int(input("Entre o número (ORD) do aluno que deseja excluir (0 - aborta):\n"))
            if ord < 0 or ord > len(lista):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break
    ord -= 1
    cpf = lista[ord][0]
    print("CPF: %s" % cpf)
    print("Nome: %s" % (lista[ord][1]))
    #   Verifica e informa sobre exclusão se aluno vinculado a alguma turma
    from crud.turmas import busca_aluno_turmas
    turmas_do_aluno = busca_aluno_turmas(cpf)
    if len(turmas_do_aluno) > 0:
        print("ATENÇÃO: o aluno acima está inscrito na(s) seguinte(s) turma(s):")
        for turma in turmas_do_aluno:
            print("\tCódigo: %s, Período: %s, Disciplina: %s %s" % (turma[1], turma[2], turma[3], turma[4]))
        print("Esta operação irá remover o aluno da(s) turma(s) acima")
    resp = input("Confirma a exclusão desse aluno?\n(sim = confirma): ")
    if resp.lower() != 'sim':
        return
    #   chama função para remover alunos de todas as turmas em que estava matriculado
    from crud.turmas import remover_aluno_geral
    remover_aluno_geral(cpf)
    #   remove aluno da lista na memória e salva cadastro no HD
    del lista[ord]
    _salvar_cadastro()


def _ler_cadastro():
    del lista[:]    # limpa lista antes de ler
    f.ler_arquivo(arquivo, lista)   # usa função acessória de leitura de arquivo no módulo ferramentas


#   salva cadastro em arquivo
def _salvar_cadastro():
    f.salvar_arquivo(arquivo, lista)    # usa função acessória de gravação de arquivo no módulo ferramentas


#   imprime cadastro em ordem alfabética por nome
def _imprime_cadastro():
    lista.sort(key=lambda cadastro: cadastro[1].lower())
    f.imprimir_tabela(cabeçalho, lista)


def acha_aluno(cpf):
    # Função para encontrar um CPF na lista;
    # retorna o cadastro na lista se o CPF do aluno existir
    # ou None se o CPF não estiver cadastrado
    for cadastro in lista:
        if cadastro[0] == cpf:
            return cadastro.copy()
    return None


def alunos():
    # loop para input de opção de menu com bloco try-except para forçar
    # o usuário a entrar uma opção válida:
    while True:
        print("Cadastro de alunos".upper())
        _imprime_cadastro()
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
opções = [("Sair", lambda _=None: True), ("Novo aluno", _novo_aluno),
          ("Alterar cadastro", _alterar_cadastro),
          ("Excluir aluno", _excluir_aluno)]

#   inicializa o módulo lendo o cadastro do arquivo para a memória
_ler_cadastro()











