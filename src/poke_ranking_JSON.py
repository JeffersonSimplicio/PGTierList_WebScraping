import concurrent.futures
from time import sleep
from src.models.poke_link_model import PokeLinkModel
from src.models.poke_attack_model import PokeAttackModel
from src.models.pokemon_model import PokemonModel
from src.scraping.web_scraper import WebScraper
from src.scraping.tier_list_abstract import TierListAbstract
from src.scraping.poke_info_scraping import PokeInfoAbstract
from src.utilities.json_handler import JsonHandler
from src.utilities.terminal import Terminal


class PokeRankingJSON:
    def __init__(
        self,
        poke_link: type[PokeLinkModel],
        poke_attack: type[PokeAttackModel],
        scraper: type[WebScraper],
        tier_list_scraping: type[TierListAbstract],
        poke_info_scraping: type[PokeInfoAbstract],
        link_base: str,
        link_tier: str,
        max_workers: int = 10,
    ) -> None:
        self.poke_attack = poke_attack
        self.scraper = scraper
        self.poke_info_scraping = poke_info_scraping
        self.link_base = link_base
        self.max_workers = max_workers

        driver = self.scraper(self.link_base + link_tier)
        self.TierList = tier_list_scraping(poke_link, driver)
        self.TierListDict = self.TierList.pokemon_by_ranking()

    # É quase impossível parar a aplicação qnd esse método é executado
    # Precisa acha r uma maneira de corrigir isso
    def generate(self) -> dict[str, list[dict[str, any]]]:
        total_pokemons = self.TierList.count_pokemon()
        poke_tier_ranking = {}

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=self.max_workers
        ) as executor:
            future_to_pokemon = {}
            for tier, poke_list in self.TierListDict.items():
                poke_tier_ranking[tier] = []
                for pokemon in poke_list:
                    future = executor.submit(
                        self.process_pokemon, pokemon["name"], pokemon["link"]
                    )
                    future_to_pokemon[future] = (tier, pokemon["name"])

            completed = 0
            for future in concurrent.futures.as_completed(future_to_pokemon):
                tier, name = future_to_pokemon[future]
                try:
                    Terminal.info("Pokemon em analise: ", name)
                    poke_data = future.result()
                    poke_tier_ranking[tier].append(poke_data)
                except Exception as e:
                    Terminal.error(f"Erro ao processar {name}: {e}")

                completed += 1
                percentage = (completed / total_pokemons) * 100
                Terminal.info(
                    f"Progresso: {completed} de {total_pokemons}",
                    f", {percentage:.2f}%"
                )

        return poke_tier_ranking

    def process_pokemon(self, name: str, link: str) -> dict:
        return self._retry_execution(name, link)

    def _retry_execution(
        self,
        name: str,
        link: str,
        attempt_limit: int = 2,
        retry_delay_seconds: int = 3
    ):
        for attempt in range(attempt_limit):
            try:
                poke_info_base = self.poke_info_scraping(
                    self.scraper(self.link_base + link), self.poke_attack
                )
                poke_data = PokemonModel(
                    name,
                    poke_info_base.get_typing(),
                    poke_info_base.is_shiny_available(),
                    poke_info_base.get_attacks(),
                )
                return poke_data.to_dict()
            except Exception as e:
                Terminal.warning(
                    f"Erro ao processar {name} (tentativa {attempt + 1}): {e}"
                )
                if attempt < attempt_limit - 1:
                    Terminal.info(
                        "Tentando novamente em ",
                        f"{retry_delay_seconds} segundos..."
                    )
                    sleep(retry_delay_seconds)
        raise Exception(
            f"Falha ao processar {name} após {attempt_limit} tentativas"
        )

    def generate_json(self, file_name: str = "pg_tier_list") -> None:
        JsonHandler(file_name).write(self.generate())
