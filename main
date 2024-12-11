from random import choice
import select
import sys
import data_analysis
import utils


def main():
    file = utils.select_file()
    utils.generate_report(file)
    data = utils.split_lines(file)

    print("\nOpções:")
    print("1: Listar candidatos")
    print("2: Listar partidos")
    print("3: Candidato com mais votos")
    print("4: Menos votados")
    print("5: Votos do Partido")
    print("6: Total de votos de uma cidade")
    print("7: Total de votos de um candidato")
    print("8: Porcentagem de Brancos ou nulos")
    print("9: Para imprimir um relatório")
    print("10: Sair")
    print("11: para Limpar a Tela")
    print("\n")
    option = int(input("Digite a opção desejada: "))
    print("\n")
    match option:
        case 1:
            print("1. Candidatos de uma cidade específica")
            print("2. Candidatos de um partido específico")
            print("3. Candidatos a prefeito")
            print("4. Candidatos a vereador")
            print("5. Todos os candidatos")
            print("0. Voltar")
            print("\n")
            choice = int(input("Digite a opção desejada: "))
            if choice == 1:
                city = input("Digite o nome da cidade: ").upper()
                print("\n")
                print("1. Partido especifico")
                print("2. Todos os partidos")
                choice2 = int(input("Digite a opção desejada: "))
                print("\n")
                print("1. Candidatos a prefeito")
                print("2. candidatos a vereador")
                print("3. Todos os candidatos")
                print("0. Voltar ao menu principal")
                choice3 = int(input("Digite a opção desejada: "))
                if choice2 == 1:
                    party = input(
                        "Digite o nome do partido: Ex. Partido Liberal, Partido dos Trabalhadores, etc. "
                    )
                    if choice3 == 1:
                        print("\n")
                        for line in utils.candidates(
                            data, city=city, party=party, position="Prefeito"
                        ):
                            print(line)
                    elif choice3 == 2:
                        print("\n")
                        for line in utils.candidates(
                            data, city=city, party=party, position="Vereador"
                        ):
                            print(line)
                    elif choice3 == 3:
                        print("\n")
                        for line in utils.candidates(data, city=city, party=party):
                            print(line)
                    else:  # choice3 == 0
                        main()
                elif choice2 == 2:
                    if choice3 == 1:
                        print("\n")
                        for line in utils.candidates(
                            data, city=city, position="Prefeito"
                        ):
                            print(line)
                    elif choice3 == 2:
                        print("\n")
                        for line in utils.candidates(
                            data, city=city, position="Vereador"
                        ):
                            print(line)
                    elif choice3 == 3:
                        print("\n")
                        for line in utils.candidates(data, city=city):
                            print(line)
                    else:  # choice3 == 0
                        main()
            elif choice == 2:
                party = input(
                    "Digite o nome do partido: Ex. Partido Liberal, Partido dos Trabalhadores, etc. "
                )
                print("\n")
                print("1. Candidatos a prefeito")
                print("2. candidatos a vereador")
                print("3. Todos os candidatos")
                print("0. Voltar ao menu principal")
                choice2 = int(input("Digite a opção desejada: "))
                if choice2 == 1:
                    print("\n")
                    for line in utils.candidates(
                        data, party=party, position="Prefeito"
                    ):
                        print(line)
                elif choice2 == 2:
                    print("\n")
                    for line in utils.candidates(
                        data, party=party, position="Vereador"
                    ):
                        print(line)
                elif choice2 == 3:
                    print("\n")
                    for line in utils.candidates(data, party=party):
                        print(line)
                else:  # choice2 == 0
                    main()
            elif choice == 3:
                print("\n")
                for line in utils.candidates(data, position="Prefeito"):
                    print(line)
            elif choice == 4:
                print("\n")
                for line in utils.candidates(data, position="Vereador"):
                    print(line)
            elif choice == 5:
                print("\n")
                for line in utils.candidates(data):
                    print(line)
            else:  # choice == 0
                main()
        case 2:
            print("\n")
            print("Partidos de uma cidade específica")
            print("1. SIM")
            print("2. NÃO")
            print("0. Voltar")
            print("\n")
            choice = int(input("Digite a opção desejada: "))
            if choice == 1:
                city = input("Digite o nome da cidade: ").upper()
                print("\n")
                for line in utils.parties(data, city=city):
                    print(line)
            elif choice == 2:
                print("\n")
                for line in utils.parties(data):
                    print(line)
            else:  # choice == 0
                main()
        case 3:
            print("\n")
            print("Em uma cidade especifica?")
            print("1. SIM")
            print("2. NÃO")
            print("0. Voltar")
            print("\n")
            choice = int(input("Digite a opção desejada: "))
            print("\n")
            print("Em um partido específico?")
            print("1. SIM")
            print("2. NÃO")
            print("0. Voltar")
            print("\n")
            choice2 = int(input("Digite a opção desejada: "))
            if choice == 1:
                city = input("Digite o nome da cidade: ").upper()
                if choice2 == 1:
                    party = input(
                        "Digite o nome do partido: Ex. Partido Liberal, Partido dos Trabalhadores, etc. "
                    )
                    print("\n")
                    for line in data_analysis.more_votes(data, city=city, party=party):
                        print(line)
                elif choice2 == 2:
                    print("\n")
                    for line in data_analysis.more_votes(data, city=city):
                        print(line)
                else:  # choice2 == 0
                    main()
            elif choice == 2:
                if choice2 == 1:
                    party = input(
                        "Digite o nome do partido: Ex. Partido Liberal, Partido dos Trabalhadores, etc. "
                    )
                    print("\n")
                    for line in data_analysis.more_votes(data, party=party):
                        print(line)
                elif choice2 == 2:
                    print("\n")
                    for line in data_analysis.more_votes(data):
                        print(line)
                else:  # choice2 == 0
                    main()
            else:  # choice == 0
                main()
        case 4:
            pass
        case 5:
            pass
        case 6:
            city = input("Digite o nome da cidade: ").upper()
            print("\n")
            print("1. Candidatos a prefeito")
            print("2. candidatos a vereador")
            print("3. Todos os candidatos")
            print("0. Voltar ao menu principal")
            choice = int(input("Digite a opção desejada: "))
            if choice == 1:
                print("\n")
                print(data_analysis.city_votes(data, city, position="Prefeito"))
            elif choice == 2:
                print("\n")
                print(data_analysis.city_votes(data, city, position="Vereador"))
            elif choice == 3:
                print("\n")
                print(data_analysis.city_votes(data, city))
            else:  # choice == 0
                main()
        case 7:
            city = input("Digite o nome da cidade: ").upper()
            candidate = input("Digite o nome do candidato: ")
            print("\n")
            print(data_analysis.city_votes(data, city, candidate))
        case 8:
            pass
        case 9:
            data_analysis.create_resume(list(data))
        case 10:
            sys.exit(0)
        case 11:
            sys.stdout.write("\x1b[2J\x1b[H")
        case _:
            pass


if __name__ == "__main__":
    main()
