from sys import exit
from time import sleep
from src.utilities.terminal import Terminal
from src.poke_ranking_handler import PokeRankingHandler
from src.poke_move_handler import PokeMoveHandler


class PokemonCLI:
    def __init__(self):
        self.options = {
            '1': self.get_pokemon_list,
            '2': self.get_moves_list,
            '3': self.get_pokemon_and_moves,
            '4': self.exit_program
        }

    def get_pokemon_list(self):
        Terminal.info("Iniciando a busca pelo ranking dos melhores Pokémon.")
        PokeRankingHandler().run()
        Terminal.success("Ranking criado com sucesso!")

    def get_moves_list(self):
        Terminal.info("Iniciando a busca por golpes.")
        PokeMoveHandler().run()
        Terminal.success("Lista de golpes criada com sucesso!")

    def get_pokemon_and_moves(self):
        self.get_moves_list()
        self.get_pokemon_list()

    def exit_program(self):
        Terminal.info("Saindo do programa. Até a proxima!")
        exit(0)

    def display_menu(self):
        print("\nPor favor, escolha uma opção:")
        print("1. Obter lista de Pokémon")
        print("2. Obter lista de golpes de Pokémon")
        print("3. Obter ambas as listas de Pokémon e golpes")
        print("4. Cancelar e sair")

    def run(self):
        while True:
            Terminal.clear()
            self.display_menu()
            choice = input("Digite sua escolha (1-4): ")
            action = self.options.get(choice)

            if action:
                action()
                break
            else:
                Terminal.warning(
                    "Escolha inválida, por favor,",
                    "insira um número entre 1 e 4."
                )
                sleep(3)


if __name__ == "__main__":
    cli = PokemonCLI()
    cli.run()
