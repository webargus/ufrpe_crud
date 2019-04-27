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
from crud.alunos import acha_aluno

#  Variáveis globais do módulo:
#
# nome do arquivo .csv para salvar as turmas
# campos de dados do arquivo:
# id_turma: chave primária, string composta pela concatenação dos 3 campos abaixo:
# codigo: código da turma, string de no máximo 4 caracteres, geralmente indicando a sala
# periodo: período da turma, string no formato aaaa.s, onde aaaa = ano e s = semestre (1 ou 2)
# codigo_disciplina: código da disciplina, conforme definido no módulo disciplinas
# A chave id_turma identifica inequivocamente uma turma, já que não pode haver duas turmas
# com os mesmos parâmetros para 'codigo', 'periodo' e 'codigo_disciplina'
turmas_geral = "turmas"

# nome do arquivo .csv para salvar os professores das turmas
# campos de dados do arquivo:
# id_turma: id única da turma, conforme descrito acima
# cpf_professor: CPF do professor vinculado à turma
# obs.: esse é um arquivo intermediário de referência entre
#       o cadastro de professores (módulo 'professores') e as turmas que leciona
turmas_profs = "turmas_professores"

# nome do arquivo .csv para salvar os alunos das turmas
# campos de dados do arquivo
# id_turma: id única da turma, conforme descrito antes
# cpf_aluno: CPF do aluno vinculado à turma
# obs.: esse é um arquivo intermediário de referência entre
#       o cadastro de alunos (módulo 'alunos') e as turmas em que o aluno está matriculado
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
# dicionário de formatação do cabeçalho de impressão da lista de alunos;
cabeçalho_alunos = {"CPF": "15", "Nome": "50"}


def _criar_turma():
    while True:
        while True:
            # Entra um código para a turma, com no máximo 4 caracteres
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
            # entra o período da turma no formato aaaa.s
            periodo = input("Entre o período da turma (Enter - aborta):\n")
            periodo = periodo.strip()
            if len(periodo) == 0:
                print("Operação abortada")
                return
            # chama função acessória (módulo 'ferramentas') para validar período
            if f.validar_periodo(periodo):
                break
            else:
                print("Período inválido (formato = aaaa.s, ex., 2019.1, 2018.2)")

        # entra disciplina
        # chama função do módulo 'disciplinas' que mostra tabela de disciplinas cadastradas
        # e retorna cópia de lista de disciplinas na memória
        disciplinas = importar_disciplinas()
        if len(disciplinas) == 0:   # aborta se não há disciplinas cadastradas
            print("***Não há disciplinas cadastradas")
            print("\tNo menu principal, escolha a opção '2 - disciplinas->1 - Nova disciplina' e cadastre a disciplina\n")
            return
        while True:     # seleciona disciplina a partir da tabela na tela
            try:
                ord = int(input("Entre o número (ORD) da disciplina (0 - aborta):\n"))
                if ord < 0 or ord > len(disciplinas):
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
        # compõe id única da disciplina a partir de seus parâmetros:
        id_turma = codigo + periodo + disciplinas[ord][0]
        # verifica se id já existe => nega inclusão de turma repetida
        turma = _acha_turma(id_turma)
        if turma is None:
            break
        else:
            print("Turma já cadastrada")

    #   inclui turma na memória e a salva em arquivo
    lista_turmas.append([id_turma, codigo, periodo, disciplinas[ord][0]])
    _salvar_turmas()


def _excluir_turma():
    if len(lista_turmas) == 0:  # aborta operação se lista de turmas vazia
        print("Cadastro de turmas vazio, não há turmas para excluir.")
        return
    while True:
        try:    # entra turma a excluir por sua referência ORD na tabela printada na tela
            ord = int(input("Entre o número (ORD) da turma que deseja excluir (0 - aborta):\n"))
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
    # printa dados da turma e pede confirmação da exclusão
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    codigo = lista_turmas[ord][3]
    print("Disciplina: %s - %s" % (codigo, acha_disciplina(codigo)[1]))
    print("ATENÇÃO! A exclusão dessa turma implica na exclusão de todos os professores e alunos a ela vinculados.")
    print("Confirma a exclusão dessa turma assim mesmo?")
    resp = input("(sim = confirma): ")
    if resp.lower() != 'sim':
        return
    # exclui todos os professores e alunos referenciados para a turma e exclui a turma
    id_turma = lista_turmas[ord][0]
    _elimina_professores(id_turma)
    _elimina_alunos(id_turma)
    del lista_turmas[ord]
    # salva a lista de turmas e as tabelas de referência de alunos e professores
    _salvar_turmas()
    _salvar_professores()
    _salvar_alunos()


def _incluir_professor():
    if len(lista_turmas) == 0:  # aborta se não há turmas cadastradas
        print("Não há turmas cadastradas para incluir professor")
        return
    while True:
        try:    # entra uma turma onde incluir o professor a partir do número ORD printado na tela
            ord = int(input("Entre o número (ORD) da turma para incluir professor (0 - aborta):\n"))
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
    print("Turma: %s" % (lista_turmas[ord][1]))
    codigo = lista_turmas[ord][3]
    print("Disciplina: %s - %s" % (codigo, acha_disciplina(codigo)[1]))
    print("Código da disciplina: %s" % (lista_turmas[ord][3]))
    id_turma = lista_turmas[ord][0]

    # printa tabela de professores cadastrados no módulo 'professores' e lê cópia do cadastro
    professores = importar_professores()
    if len(professores) == 0:   # aborta se cadastro vazio
        print("***Não há professores cadastrados")
        print("\tNo menu principal, escolha a opção '1 - professores -> 1 - Novo cadastro' e cadastre professor\n")
        return
    while True:
        try:    # seleciona professor a partir de seu número de ordem printado na tela
            ord = int(input("Entre o número (ORD) do professor (0 - aborta):\n"))
            if ord < 0 or ord > len(professores):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ord == 0:
            print("Operação abortada")
            return
        break

    ord -= 1
    # printa dados do professor selecionado
    cpf = professores[ord][0]
    print("CPF: %s" % cpf)
    print("Nome: %s" % (professores[ord][1]))
    # verifica se professor já vinculado à turma e aborta se for o caso
    profs = _acha_professores(id_turma)
    for prof in profs:
        if prof[0] == cpf:
            print("Esse professor já está a cargo dessa turma.")
            return
    # vincula professor à turma na memória e salva arquivo de referência no HD
    lista_profs.append([id_turma, cpf])
    _salvar_professores()


def _excluir_professor():
    if len(lista_turmas) == 0:  # aborta se não há turmas cadastradas
        print("Não há turmas cadastradas para excluir professor")
        return
    while True:
        try:    # entra turma do professor baseado no número de ordem printado na tela
            ordem = int(input("Entre o número (ORD) da turma do professor (0 - aborta):\n"))
            if ordem < 0 or ordem > len(lista_turmas):
                raise ValueError
        except ValueError:
            print("Entrada inválida :( tente novamente...")
            continue
        if ordem == 0:
            print("Operação abortada")
            return
        break
    ordem -= 1
    # exibe dados da turma
    id_turma = lista_turmas[ordem][0]
    print("Turma: %s" % (lista_turmas[ordem][1]))
    print("Período: %s" % (lista_turmas[ordem][2]))
    codigo = lista_turmas[ordem][3]
    print("Disciplina: %s - %s" % (codigo, acha_disciplina(codigo)[1]))
    #   busca por professores da turma pela id da turma
    professores = _acha_professores(id_turma)
    if len(professores) == 0:   # aborta se a turma não tem professores vinculados à ela
        print("Não há professores designados para essa turma.")
        return
    # exibe lista de professor(es) e entra número de ordem que o identifica na listagem printada,
    # no caso de haver mais de um professor designado para a turma
    pos = 0
    if len(professores) > 1:
        print("Professores:")
        for indice in range(len(professores)):
            print("\t%d - %s" % (indice + 1, professores[indice][1]))
        while True:
            try:
                pos = int(input("Remover qual professor (de 1 a %d):" % (len(professores))))
                if pos < 1 or pos > len(professores):
                    raise ValueError
                else:
                    pos -= 1
                    break
            except ValueError:
                print("Entrada inválida :(")
    # pede pela confirmação da exclusão do professor selecionado
    print("Remover professor: %s" % (professores[pos][1]))
    resp = input("Confirma a remoção (sim - remove)?")
    if resp.lower() != 'sim':
        return
    # remove professor
    _remover_professor(id_turma, professores[pos][0])


def _incluir_aluno():
    if len(lista_turmas) == 0:  # aborta se não houver turmas cadastradas
        print("Não há turmas para incluir aluno")
        return
    while True:
        try:    # entra turma na qual se quer incluir o aluno, pelo número ORD da turma na tela
            ord = int(input("Entre o número (ORD) da turma para incluir o aluno (0 - aborta):\n"))
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
    # exibe dados da turma
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    codigo = lista_turmas[ord][3]
    print("Disciplina: %s - %s" % (codigo, acha_disciplina(codigo)[1]))
    # exibe alunos da turma, se houver
    id_turma = lista_turmas[ord][0]
    if len([x for x in lista_alunos if x[0] == id_turma]) > 0:
        print("Alunos matriculados na turma:")
        _imprimir_alunos(id_turma)

    # entra e valida CPF do aluno a incluir
    while True:
        cpf = input("Entre o CPF do aluno (0 - aborta):\n")
        if cpf == "0":
            print("Operação abortada")
            return
        if f.validar_cpf(cpf):
                break
        else:
            print("CPF inválido (somente algarismos, 11 dígitos): tente novamente")
    # formata e verifica se existe aluno cadastrado com o CPF fornecido
    cpf = f.formatar_cpf(cpf)
    aluno = acha_aluno(cpf)
    if aluno is None:
        print("Não há aluno cadastrado com o CPF %s" % cpf)
        print("\tNo menu principal, escolha a opção '3 - Alunos -> 1 - Novo aluno' e cadastre o aluno\n")
        return
    # vê se aluno já foi incluido na turma e aborta se for o caso
    print("CPF: %s" % aluno[0])
    print("Nome: %s" % (aluno[1]))
    if _checa_aluno(cpf, id_turma):
        print("Esse aluno já foi incluído na turma.")
        return
    # inclui aluno na turma
    lista_alunos.append([id_turma, cpf])
    _salvar_alunos()
    # exibe lista atualizada de alunos da turma
    print("Alunos matriculados na turma:")
    _imprimir_alunos(id_turma)


def _excluir_aluno():
    if len(lista_turmas) == 0:      # aborta se não há turmas cadastradas
        print("Não há turmas para excluir aluno")
        return
    while True:
        try:  # entra a turma de onde se quer excluir o aluno, pelo número de ordem mostrado na tela
            ord = int(input("Entre o número (ORD) da turma de onde excluir o aluno (0 - aborta):\n"))
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
    # exibe dados da turma
    print("Turma: %s" % (lista_turmas[ord][1]))
    print("Período: %s" % (lista_turmas[ord][2]))
    codigo = lista_turmas[ord][3]
    print("Disciplina: %s - %s" % (codigo, acha_disciplina(codigo)[1]))
    id_turma = lista_turmas[ord][0]
    # exibe lista de alunos da turma e obtém cópia da lista
    print("Alunos matriculados na turma:")
    lista = _imprimir_alunos(id_turma)
    if len(lista) == 0:     # aborta exclusão se não há alunos a excluir da turma
        print("Não há alunos inscritos nessa turma")
        return
    while True:
        try:    # entra aluno a excluir baseado no número de ordem correspondente na lista de alunos printada na tela
            ord = int(input("Entre o número (ORD) do aluno a excluir (0 - aborta):\n"))
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
    # exibe dados do aluno e pede pela confirmação da exclusão
    cpf = lista[ord][0]
    print("CPF: %s" % cpf)
    print("Nome: %s" % lista[ord][1])
    resp = input("Confirma a remoção do aluno (sim - remove)?")
    if resp.lower() != 'sim':
        return
    # remove aluno e imprime tabela atualizada dos alunos da turma
    _remover_aluno(cpf, id_turma)
    _imprimir_alunos(id_turma)


def _remover_professor(id_turma, cpf):
    # remove da tabela associativa a referência para o professor identificado por cpf
    for entrada in lista_profs:
        if entrada[0] == id_turma and entrada[1] == cpf:
            lista_profs.remove(entrada)
            _salvar_professores()
            break


def _elimina_professores(id_turma):
    # função (recursiva) para excluir a(s) referência(s) para todos os professores da turma identificada por id_turma
    for entrada in lista_profs:
        if entrada[0] == id_turma:
            lista_profs.remove(entrada)
            _elimina_professores(id_turma)


def _elimina_alunos(id_turma):
    # função (recursiva) para desvincular todos os alunos referenciados à turma id_turma
    for entrada in lista_alunos:
        if entrada[0] == id_turma:
            lista_alunos.remove(entrada)
            _elimina_alunos(id_turma)


def _ler_turmas():
    # lê as turmas do arquivo .csv no HD para a memória
    del lista_turmas[:]    # limpa lista antes de ler
    f.ler_arquivo(turmas_geral, lista_turmas)   # usa função de leitura de arquivo definida no módulo 'ferramentas'


def _salvar_turmas():
    # salva lista de turmas no HD usando função de escrita em arquivo definida no módulo 'ferramentas'
    f.salvar_arquivo(turmas_geral, lista_turmas)


def _ler_professores():
    # lê tabela associativa entre professores e turmas do arquivo .csv no HD para a memória
    del lista_profs[:]  # limpa memória antes de ler
    f.ler_arquivo(turmas_profs, lista_profs)    # usa função de leitura de arquivo definida no módulo 'ferramentas'


def _salvar_professores():
    # salva tabela associativa entre professores e turmas no HD usando função de escrita em arquivo definida em 'ferramentas'
    f.salvar_arquivo(turmas_profs, lista_profs)


def _ler_alunos():
    # lê tabela associativa entre alunos e turmas, do HD para a memória
    del lista_alunos[:]     # limpa memória antes de ler
    f.ler_arquivo(turmas_alunos, lista_alunos)  # usa função de leitura de arquivo definida em 'ferramentas'


def _salvar_alunos():
    # salva tabela de referência entre alunos e turmas no HD usando função de escrita em arquivo definida em 'ferramentas'
    f.salvar_arquivo(turmas_alunos, lista_alunos)


def _exportar_turmas():
    # exporta cópia de lista de turmas usando função de cópia definida no módulo 'ferramentas'
    # (função importada pelo módulo 'relatorios' para a emissão de reportes)
    return f.copiar_lista(lista_turmas)


def _exportar_professores():
    # exporta cópia de lista de referência entre professores e turmas
    # usando função de cópia definida no módulo 'ferramentas'
    # (função importada pelo módulo 'relatorios' para a emissão de reportes)
    return f.copiar_lista(lista_profs)


def _exportar_alunos():
    # exporta cópia de lista de referência entre alunos e turmas usando função de cópia definida no módulo 'ferramentas'
    # (função importada pelo módulo 'relatorios' para a emissão de reportes)
    return f.copiar_lista(lista_alunos)


def _acha_turma(id_turma):
    # busca turma por id da turma e retorna tupla com dados da turma
    # ou None se turma não encontrada
    turma_copia = f.copiar_lista(lista_turmas)
    for turma in turma_copia:
        if turma[0] == id_turma:
            return turma.copy()
    return None


def _acha_professores(id_turma):
    # retorna lista contendo os cadastros dos professores pertencentes á turma identificada por id_turma
    professores = []
    profs_copia = f.copiar_lista(lista_profs)
    for entrada in profs_copia:
        if entrada[0] == id_turma:
            # usa função definida no módulo 'professores' para fazer busca do cadastro do professor
            prof = acha_professor(entrada[1])
            if prof is not None:
                professores.append(prof.copy())     # acumula cadastro encontrado na lista de retorno
    return professores


def acha_turmas_professor(cpf):
    # busca e retorna turmas às quais o professor identificado por cpf está vinculado, baseando-se
    # na lista associativa entre professores e turmas (lista 'turmas_professor')
    turmas_professor = []
    profs_copia = f.copiar_lista(lista_profs)
    for entrada in profs_copia:
        if entrada[1] == cpf:       # bingo! achou turma associada ao professor
            turma = _acha_turma(entrada[0])     # usa função local para ler cadastro da turma
            # busca cadastro da disciplina correspondente à turma usando função importada do módulo 'disciplinas'
            turma.append(acha_disciplina(turma[3])[1])  # acrescenta nome por extenso da disciplina ao cadastro lido
            turmas_professor.append(turma.copy())   # acumula turma na lista de retorno
    return turmas_professor


def busca_turmas_disciplina(codigo):
    # busca e retorna lista contendo turmas vinculadas à disciplina identificada por 'codigo'
    turmas = []
    turmas_copia = f.copiar_lista(lista_turmas)
    for turma in turmas_copia:
        if turma[3] == codigo:
            turmas.append(turma.copy())
    return turmas


def busca_aluno_turmas(cpf):
    # busca e retorna as turmas em que o aluno identificado por cpf está matriculado
    turmas_do_aluno = []
    turmas_copia = f.copiar_lista(lista_turmas)
    for turma in turmas_copia:      # varre as turmas em busca do aluno
        if _checa_aluno(cpf, turma[0]):     # vê se aluno está matriculado na turma
            turma.append(acha_disciplina(turma[3])[1])      # acrescenta nome da disciplina ao cadastro da turma
            turmas_do_aluno.append(turma.copy())    # acumula cadastro da turma na lista de retorno
    return turmas_do_aluno


def _checa_aluno(cpf, id_turma):
    # verifica se o aluno identificado por 'cpf' pertence à turma identificada por 'id_turma'
    # retorna verdadeiro ou falso, conforme o caso
    for aluno in lista_alunos:
        if aluno[0] == id_turma and aluno[1] == cpf:
            return True
    return False


def remover_aluno_geral(cpf):
    # remove o aluno identificado por 'cpf' de todas as turmas e salva lista de referência entre alunos e turmas no HD
    for turma in lista_turmas:
        _remover_aluno(cpf, turma[0], False)    # False => não salve lista no HD ainda, só no final da remoção
    _salvar_alunos()


def _remover_aluno(cpf, id_turma, salva=True):
    # remove aluno da lista associativa entre alunos e turmas e salva lista no HD se parâmetro de entrada salva = True
    for aluno in lista_alunos:
        if aluno[0] == id_turma and aluno[1] == cpf:    # bingo! associação encontrada entre aluno e turma
            lista_alunos.remove(aluno)      # remove o aluno
            break
    if salva:
        _salvar_alunos()


def _imprimir_alunos(id_turma):
    # imprime tabela mostrando os alunos matriculados na turma identificada por 'id_turma'
    lista = [x for aluno in lista_alunos if aluno[0] == id_turma for x in [acha_aluno(aluno[1])]]
    f.imprimir_tabela(cabeçalho_alunos, lista)
    return lista


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
    # ordena lista por período da turma
    lista.sort(key=lambda turma: turma[1])
    f.imprimir_tabela(cabeçalho_turmas, lista)


def _inicializa():
    #   inicializa o módulo lendo os cadastros de turmas do arquivo para a memória
    _ler_alunos()
    _ler_professores()
    _ler_turmas()


def turmas():
    _inicializa()
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
          ("Criar turma", _criar_turma),
          ("Excluir turma", _excluir_turma),
          ("Incluir professor", _incluir_professor),
          ("Excluir professor", _excluir_professor),
          ("Incluir aluno", _incluir_aluno),
          ("Excluir aluno", _excluir_aluno)]

_inicializa()


















