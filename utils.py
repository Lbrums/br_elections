import csv as csv
import os as os
import sys as sys
from collections import defaultdict

"""
Indices da lista de valores de cada linha do arquivo .csv
0: DT_GERACAO
1: HH_GERACAO
2: ANO_ELEICAO
3: CD_TIPO_ELEICAO
4: NM_TIPO_ELEICAO
5: CD_PLEITO
6: DT_PLEITO
7: NR_TURNO
8: CD_ELEICAO
9: DS_ELEICAO
10: SG_UF
11: CD_MUNICIPIO
12: NM_MUNICIPIO
13: NR_ZONA
14: NR_SECAO
15: NR_LOCAL_VOTACAO
16: CD_CARGO_PERGUNTA
17: DS_CARGO_PERGUNTA
18: NR_PARTIDO
19: SG_PARTIDO
20: NM_PARTIDO
21: DT_BU_RECEBIDO
22: QT_APTOS
23: QT_COMPARECIMENTO
24: QT_ABSTENCOES
25: CD_TIPO_URNA
26: DS_TIPO_URNA
27: CD_TIPO_VOTAVEL
28: DS_TIPO_VOTAVEL
29: NR_VOTAVEL
30: NM_VOTAVEL
31: QT_VOTOS
32: NR_URNA_EFETIVADA
33: CD_CARGA_1_URNA_EFETIVADA
34: CD_CARGA_2_URNA_EFETIVADA
35: CD_FLASHCARD_URNA_EFETIVADA
36: DT_CARGA_URNA_EFETIVADA
37: DS_CARGO_PERGUNTA_SECAO
38: DS_SECOES_AGREGADAS
39: DT_ABERTURA
40: DT_ENCERRAMENTO
41: QT_ELEI_BIOM_SEM_HABILITACAO
42: DT_EMISSAO_BU
43: NR_JUNTA_APURADORA
44: NR_TURMA_APURADORA
"""


def select_file():
    print("Selecione o arquivo de boletins de urna:")

    # Diretório contendo os arquivos
    directory = "boletins_de_urna"
    try:
        # Listando arquivos com extensão .csv
        available_files = [
            file for file in os.listdir(directory) if file.endswith(".csv")
        ]
        if not available_files:
            print(f"Não há arquivos .csv disponíveis no diretório '{directory}'.")
            sys.exit(1)

        # Exibindo os arquivos com seus índices
        print("Estados disponíveis:")
        for index, file in enumerate(available_files, start=1):
            print(f"{index}: {file.split("_")[2]}")

        # Solicitando ao usuário que escolha um arquivo pelo índice
        choice = input("Digite o número correspondente ao estado desejado: ")
        if not choice.isdigit() or int(choice) not in range(
            1, len(available_files) + 1
        ):
            print("Escolha inválida.")
            sys.exit(1)

        file_path = os.path.join(directory, available_files[int(choice) - 1])

        return file_path

    except FileNotFoundError:
        print(f"Erro: O diretório '{directory}' não foi encontrado.")
        sys.exit(1)


# função para contar as linhas do arquivo
def count_lines(file_path):
    with open(file_path, "r") as file:
        return sum(1 for line in file)


# função para contar as colunas do arquivo
def columns_count(file_path):
    with open(file_path, "r", encoding="latin-1") as file:
        colunas = file.readline().strip().replace('"', "").split(";")
        return colunas


# função para gerar um relatório com alguns dados do arquivo selecionado
def generate_report(file_path):
    # Captura os nomes das colunas
    columns = columns_count(file_path)
    # Conta o número total de linhas
    total_lines = count_lines(file_path) - 1

    print(f"\nBoletim de Urna '{file_path}':")
    print("-" * 30)
    print(f"Total de linhas (excluindo o cabeçalho): {total_lines}")
    print("\nNomes das Colunas:")
    for index, column in enumerate(columns, start=1):
        print(f"{index}: {column}")


# função para filtrar os dados do arquivo e separar as linhas
def split_lines(file_path):
    with open(file_path, "r", encoding="latin-1") as file:
        # Pula a primeira linha (cabeçalho)
        next(file)
        for lines in (line.strip().replace('"', "").split(";") for line in file):
            yield lines


# função para listar os candidatos
def candidates(data, city=None, position=None, party=None):
    # Se não for passado nenhum argumento, retorna todos os candidatos
    if city is None and position is None and party is None:
        candidates = defaultdict(int)  # Default para int é 0
        for line in data:
            candidate = line[30]
            if candidate and candidate != "#NULO#":
                candidates[candidate] += 1
        return candidates
    # Se for passado apenas a cidade, retorna os candidatos da cidade
    elif city is not None and position is None and party is None:
        candidates = defaultdict(int)
        for line in data:
            if line[12] == city:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado apenas a posição, retorna os candidatos da posição
    elif city is None and position is not None and party is None:
        candidates = defaultdict(int)
        for line in data:
            if line[17] == position:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado apenas o partido, retorna os candidatos do partido
    elif city is None and position is None and party is not None:
        candidates = defaultdict(int)
        for line in data:
            if line[20] == party:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado a cidade e a posição, retorna os candidatos da cidade e posição
    elif city is not None and position is not None and party is None:
        candidates = defaultdict(int)
        for line in data:
            if line[12] == city and line[17] == position:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado a cidade e o partido, retorna os candidatos da cidade e partido
    elif city is not None and position is None and party is not None:
        candidates = defaultdict(int)
        for line in data:
            if line[12] == city and line[20] == party:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado a posição e o partido, retorna os candidatos da posição e partido
    elif city is None and position is not None and party is not None:
        candidates = defaultdict(int)
        for line in data:
            if line[17] == position and line[20] == party:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates
    # Se for passado a cidade, posição e partido, retorna os candidatos da cidade, posição e partido
    else:
        candidates = defaultdict(int)
        for line in data:
            if line[12] == city and line[17] == position and line[20] == party:
                candidate = line[30]
                if candidate and candidate != "#NULO#":
                    candidates[candidate] += 1
        return candidates


# função para listar os partidos
def parties(data, city=None):
    # Se não for passado nenhum argumento, retorna todos os partidos
    if city is None:
        parties = defaultdict(int)
        for line in data:
            party = line[20]
            if party and party != "#NULO#":
                parties[party] += 1
        return parties
    # Se for passado a cidade, retorna os partidos presentes na da cidade
    else:
        parties = defaultdict(int)
        for line in data:
            if line[12] == city:
                party = line[20]
                if party and party != "#NULO#":
                    parties[party] += 1
        return parties
