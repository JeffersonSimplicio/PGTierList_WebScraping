from time import sleep
from src.models.poke_link_model import PokeLinkModel
from src.models.poke_attack_model import PokeAttackModel
from src.models.pokemon_model import PokemonModel
from src.scraping.web_scraper import WebScraper
from src.scraping.tier_list_abstract import TierListAbstract
from src.scraping.poke_info_scraping import PokeInfoAbstract
from src.utilities.json_handler import JsonHandler


class PokeRankingJSON:
    def __init__(
        self,
        poke_link: type[PokeLinkModel],
        poke_attack: type[PokeAttackModel],
        scraper: type[WebScraper],
        tier_list_scraping: type[TierListAbstract],
        poke_info_scraping: type[PokeInfoAbstract],
        link_base: str,
        link_tier: str
    ) -> None:
        self.poke_attack = poke_attack
        self.scraper = scraper
        self.poke_info_scraping = poke_info_scraping
        self.link_base = link_base

        driver = self.scraper(self.link_base + link_tier)
        self.TierList = tier_list_scraping(poke_link, driver)
        self.TierListDict = self.TierList.pokemon_by_ranking()

    def generate(self) -> dict[str, list[dict[str, any]]]:
        counter = 0
        total_pokemons = self.TierList.count_pokemon()
        percentage = (counter / total_pokemons) * 100
        poke_tier_ranking = {}
        for tier, poke_list in self.TierListDict.items():
            print(f"Tier: {tier}")
            tmp_tier_list = []
            for pokemon in poke_list:
                name: str = pokemon["name"]
                link: str = pokemon["link"]
                counter += 1
                percentage = (counter / total_pokemons) * 100
                print(f"Pokemon atual: {name}")
                print(f"{counter} de {total_pokemons}, {percentage:.2f}%")
                print(f"Resta: {total_pokemons-counter}")
                poke_data = self.retry_execution(name, link)
                tmp_tier_list.append(poke_data)
            poke_tier_ranking[tier] = tmp_tier_list
        return poke_tier_ranking

    def retry_execution(
        self,
        name: str,
        link: str,
        attempt_limit: int = 2,
        retry_delay_seconds: int = 3
    ):
        attempt = 0  # Contador de tentativas
        success = False  # Flag de sucesso

        while attempt < attempt_limit and not success:
            try:
                poke_info_base = self.poke_info_scraping(
                    self.scraper(self.link_base + link),
                    self.poke_attack
                )
                poke_data = PokemonModel(
                    name,
                    poke_info_base.get_typing(),
                    poke_info_base.is_shiny_available(),
                    poke_info_base.get_attacks(),
                )
                success = True  # Se a execução chegar aqui, foi bem-sucedida
                return poke_data.to_dict()
            except Exception as e:
                print(f"Erro ao processar {name}: {e}")
                print("Tentando novamente em 3 segundos...")
                attempt += 1
                # Espera {retry_delay_seconds} segundos
                # antes de tentar novamente
                sleep(retry_delay_seconds)

    def generate_json(self, file_name: str = "pg_tier_list") -> None:
        JsonHandler(file_name).write(self.generate())
