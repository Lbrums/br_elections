import utils
from collections import defaultdict


# Função para retornar o candidato com mais votos e o numero de votos
def more_votes(data, city=None, party=None, position=None):
    # Dicionário para armazenar votos por candidato
    votes = defaultdict(int)

    # Iteração pelos dados para acumular votos
    for line in data:
        if (
            (city is None or line[12] == city)
            and (party is None or line[20] == party)
            and (position is None or line[17] == position)
        ):
            candidate = line[30]
            if candidate and candidate not in {
                "Branco",
                "Nulo",
                "PL",
            }:  # Temos que excluir os Votos de Legenda de todos os partidos.
                votes[candidate] += int(line[31])

    candidate_with_most_votes = max(votes, key=votes.get)
    return candidate_with_most_votes, votes[candidate_with_most_votes]


# Função para retornar os candidato com menos votos e o numero de votos(Geralmente 1 voto)
def less_votes(data, city=None, party=None):
    # Dicionário para armazenar votos por candidato, cada chave terá uma lista com 2 elementos:
    # [total de votos, cidade associada]
    votes = defaultdict(lambda: [0, None])

    # Iteração pelos dados para acumular votos
    for line in data:
        # Filtra pelos critérios de cidade e partido
        if (city is None or line[12] == city) and (party is None or line[20] == party):
            candidate = line[30]
            if candidate and candidate not in {"Branco", "Nulo"}:
                # Acumula os votos e armazena a cidade associada
                votes[candidate][0] += int(line[31])
                # Registra a cidade apenas na primeira vez que o candidato é encontrado
                if votes[candidate][1] is None:
                    votes[candidate][1] = line[12]

    # Após acumular todos os votos, exclui candidatos com mais de 1 voto
    candidates_to_remove = [
        candidate for candidate, (vote_count, _) in votes.items() if vote_count > 1
    ]
    for candidate in candidates_to_remove:
        del votes[candidate]

    # Quando nenhuma cidade for passada, vamos salvar a cidade de cada candidato
    if city is None:
        cities_with_single_vote = defaultdict(list)

        for candidate, (vote_count, from_city) in votes.items():
            if vote_count == 1:
                cities_with_single_vote[from_city].append(candidate)

        # Retorna as cidades e seus respectivos candidatos com apenas 1 voto
        return cities_with_single_vote

    # Encontrar o menor número de votos
    least_votes = min(votes.values(), key=lambda x: x[0])[0]

    # Encontrar todos os candidatos com o menor número de votos
    candidates_with_least_votes = [
        candidate
        for candidate, (vote_count, _) in votes.items()
        if vote_count == least_votes
    ]

    return candidates_with_least_votes, least_votes


# Função para retornar o total de votos de um candidato
def total_candidates_with_one_vote(less_votes_data):
    return sum(len(candidates) for candidates in less_votes_data.values())


# Função para retornar os votos de um partido nas cidades
def cities_party_votes(data, party):
    # Para ordenar as cidades use:
    #         cities = sorted(
    #     list(cities_party_votes(data, input("Partido: ")).items()),
    #     key=lambda x: x[1],
    #     reverse=True,
    # )

    # Dicionário para armazenar votos por cidade
    city_votes_dict = defaultdict(int)

    # Iteração pelos dados para acumular votos por cidade para o partido especificado
    for line in data:
        partido = line[20].strip()  # Nome do partido
        cidade = line[12].strip()  # Nome da cidade
        if (
            partido.lower() == party.lower()
        ):  # Comparação insensível a maiúsculas/minúsculas
            votos = int(line[31])  # Votos
            city_votes_dict[cidade] += votos  # Acumula os votos por cidade

    return dict(city_votes_dict)  # Retorna o dicionário com os votos por cidade


# Função na cidade com diversos opções de filtros
def city_votes(
    data,
    city,
    candidate=None,
    position="Prefeito",
):
    # Variável para armazenar o total de votos da cidade específica

    total_votes = 0

    # Iterar pelos dados
    for line in data:
        if line[17] == position:  # Verifica se é uma linha de votos para prefeito
            if line[12] == city:  # Verifica se a cidade corresponde
                if candidate is not None and line[30] == candidate:
                    votes = int(line[31])  # Quantidade de votos
                    total_votes += votes  # Acumula os votos para a cidade
                elif candidate is None:
                    votes = int(line[31])  # Quantidade de votos
                    total_votes += votes  # Acumula os votos para a cidade

    return total_votes


# Função para retornar o total de votos no estado
def total_votes(data):
    total_votes = 0
    for line in data:
        if line[17] == "Prefeito":
            total_votes += int(line[31])
    return total_votes


# Função para retornar o total de votos nulos
def total_null_votes_percentage(data, position):
    # Variáveis para armazenar o total de votos e votos nulos
    total_votes_local = 0
    total_null_votes = 0
    for line in data:
        if line[17] == position:
            total_votes_local += int(line[31])
        if line[17] == position and line[30] == "Nulo":
            total_null_votes += int(line[31])
    return (total_null_votes / total_votes_local) * 100


# Função para retornar o total de votos brancos
def total_blank_votes_percentage(data, position):
    # Variáveis para armazenar o total de votos e votos em branco
    total_votes_local = 0
    total_blank_votes = 0
    for line in data:
        if line[17] == position:
            total_votes_local += int(line[31])
        if line[17] == position and line[30] == "Branco":
            total_blank_votes += int(line[31])
    return (total_blank_votes / total_votes_local) * 100


# Função para retornar a porcentagem de votos brancos de uma cidade
def blank_percentge(data, city, position):
    # Variáveis para armazenar o total de votos e votos em branco
    total_votes = city_votes(
        data,
        city,
    )
    blank_votes = city_votes(
        data,
        city,
        "Branco",
        position,
    )
    return (blank_votes / total_votes) * 100


# Função para retornar a porcentagem de votos nulos de uma cidade
def null_percentage(data, city, position):
    # Variáveis para armazenar o total de votos e votos nulos
    total_votes = city_votes(data, city)
    null_votes = city_votes(data, city, "Nulo", position)
    return (null_votes / total_votes) * 100


# Função para retornar a média proporcional de votos nulos
def null_average_proportional(data, position, cities):
    # Pegar cada cidade que existir em line[12] passar as funções null_percentage() e total_votes() e fazer a média
    # dos valores retornados
    null_percentages = []  # Lista para armazenar as porcentagens de votos nulos
    for city in cities:
        percentage = null_percentage(data, city, position)
        print("Porcentagem de votos nulos em", city, ":", percentage, "%")
        null_percentages.append(percentage)
    return sum(null_percentages) / len(null_percentages)


# Função para retornar a média proporcional de votos brancos
def blank_average_proportional(data, position, cities):
    # Pegar cada cidade que existir em line[12] passar as funções blank_percentage() e total_votes() e fazer a média
    # dos valores retornados
    blank_percentages = []  # Lista para armazenar as porcentagens de votos em branco
    for city in cities:
        percentage = blank_percentge(data, city, position)
        print("Porcentagem de votos em branco em", city, ":", percentage, "%")
        blank_percentages.append(percentage)
    return sum(blank_percentages) / len(blank_percentages)


# Função para criar um arquivo com dados selecionados
def create_resume(data):
    print("Criando variaveis locais para criação do arquivo.")
    data = list(data)
    # Lista dos dados que serão inseridos
    datafile = []

    # Solicita ao usuário os dados que estarão presentes no arquivo parcial
    city = input(
        "Digite o nome de uma cidade especifica ou 0 para fazer de todo o estado: "
    )
    if city != "0":
        print("\n")
        print("Opções:")
        print("1: Nome dos Partidos")
        print("2: Total de votos")
        print("3: Porcentagem de votos Nulos")
        print("4: Porcentagem de votos Brancos")
    else:
        print("\n")
        print("Opções:")
        print("1: Nome dos Partidos")
        print("2: Total de votos")
        print("3: Porcentagem de votos Nulos para prefeito")
        print("4: Porcentagem de votos nulos para vereador")
        print("5: porcentagem de votos brancos para vereador")
        print("6: Porcentagem de votos Brancos para prefeito")
        print("7: Média da porcentagem de Nulos para prefeito das cidades.")
        print("8: Média da porcentagem de Brancos para prefeito das cidades.")
        print("9: Média da porcentagem de Nulos para vereador das cidades.")
        print("10: Média da porcentagem de Brancos para vereador das cidades.")
    print("\n")
    choice = input("Digite as opções desejadas: ").split(",")
    print("\n")
    txt_name = input("Digite o nome do arquivo a ser gerado: ")
    print("\n")
    print("Gerando arquivo...")

    for opt in choice:
        if opt == "1":
            datafile.append("\nPARTIDOS")
            for i in (
                utils.parties(data, city=city) if city != "0" else utils.parties(data)
            ):
                datafile.append(i)
        elif opt == "2":
            datafile.append("\nTOTAL DE VOTOS")
            if city == "0":
                datafile.append(total_votes(data))
            else:
                datafile.append(city_votes(data, city))
        elif opt == "3":
            datafile.append("\nPORCENTAGEM DE VOTOS NULOS PARA PREFEITO")
            datafile.append(
                null_percentage(data, city=city, position="Prefeito")
                if city != "0"
                else total_null_votes_percentage(data, "Prefeito")
            )
        elif opt == "4":
            datafile.append("\nPORCENTAGEM DE VOTOS NULOS PARA VEREADOR")
            datafile.append(
                null_percentage(data, city=city, position="Vereador")
                if city != "0"
                else total_null_votes_percentage(data, "Vereador")
            )
        elif opt == "5":
            datafile.append("\nPORCENTAGEM DE VOTOS BRANCOS PARA VEREADOR")
            datafile.append(
                blank_percentge(data, city, "Vereador")
                if city != "0"
                else total_blank_votes_percentage(data, "Vereador")
            )
        elif opt == "6":
            datafile.append("\nPORCENTAGEM DE VOTOS BRANCOS PARA PREFEITO")
            datafile.append(
                blank_percentge(data, city, "Prefeito")
                if city != "0"
                else total_blank_votes_percentage(data, "Prefeito")
            )
        elif opt == "7":
            datafile.append("\nMÉDIA DA PORCENTAGEM DE NULOS PARA PREFEITO DAS CIDADES")
            if city == "0":
                datafile.append(
                    null_average_proportional(
                        data, "Prefeito", set(line[12] for line in data)
                    )
                )
        elif opt == "8":
            datafile.append(
                "\nMÉDIA DA PORCENTAGEM DE BRANCOS PARA PREFEITO DAS CIDADES"
            )
            if city == "0":
                datafile.append(
                    blank_average_proportional(
                        data, "Prefeito", set(line[12] for line in data)
                    )
                )
        elif opt == "9":
            datafile.append("\nMÉDIA DA PORCENTAGEM DE NULOS PARA VEREADOR DAS CIDADES")
            if city == "0":
                datafile.append(
                    null_average_proportional(
                        data, "Vereador", set(line[12] for line in data)
                    )
                )
        elif opt == "10":
            datafile.append(
                "\nMÉDIA DA PORCENTAGEM DE BRANCOS PARA VEREADOR DAS CIDADES"
            )
            if city == "0":
                datafile.append(
                    blank_average_proportional(
                        data, "Vereador", set(line[12] for line in data)
                    )
                )

    # Criação do arquivo
    with open(f"{txt_name}.txt", "w") as file:
        for line in datafile:
            file.write(str(line) + "\n")
    print("Arquivo gerado com sucesso.")
