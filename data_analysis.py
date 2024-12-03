from numpy import less
import utils
from collections import defaultdict


def more_votes(data, city=None, party=None):
    # Dicionário para armazenar votos por candidato
    votes = defaultdict(int)

    # Iteração pelos dados para acumular votos
    for line in data:
        if (city is None or line[12] == city) and (party is None or line[20] == party):
            candidate = line[30]
            if candidate and candidate not in {"Branco", "Nulo"}:
                votes[candidate] += int(line[31])

    candidate_with_most_votes = max(votes, key=votes.get)
    return candidate_with_most_votes, votes[candidate_with_most_votes]


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


def total_candidates_with_one_vote(less_votes_data):
    return sum(len(candidates) for candidates in less_votes_data.values())


def cities_party_votes(data, party):
    # Para ordenar as cidades use:
    #         cities = sorted(
    #     list(cities_party_votes(data, input("Partido: ")).items()),
    #     key=lambda x: x[1],
    #     reverse=True,
    # )

    # Dicionário para armazenar votos por cidade
    city_votes = defaultdict(int)

    # Iteração pelos dados para acumular votos por cidade para o partido especificado
    for line in data:
        partido = line[20].strip()  # Nome do partido
        cidade = line[12].strip()  # Nome da cidade
        if (
            partido.lower() == party.lower()
        ):  # Comparação insensível a maiúsculas/minúsculas
            votos = int(line[31])  # Votos
            city_votes[cidade] += votos  # Acumula os votos por cidade

    return dict(city_votes)  # Retorna o dicionário com os votos por cidade
