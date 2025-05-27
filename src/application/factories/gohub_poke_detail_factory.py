from src.domain.entities.pokemon import Pokemon
from src.application.protocols.factory import Factory

from src.domain.constants.keyword_categories import all_keyword_categories
from src.domain.services.sanitization.poke_name_sanitizer import (
    PokeNameSanitizer
)
from src.domain.services.categorization.pokemon_categorizer import (
    PokemonCategorizer
)

from src.application.assemblers.pokemon_assembler import PokemonAssembler

from src.infra.scraping.selenium_html_scraper import SeleniumHtmlScraper
from src.infra.adapter.beautiful_soup_html_adapter import (
    BeautifulSoupHtmlAdapter
)
from src.infra.poke_api.poke_api_url_generator import PokeApiUrlGenerator
from src.infra.use_case.fetch_gohub_pokemon_detail \
    .fetch_gohub_pokemon_detail_use_case import (
        FetchGoHubPokemonDetailUseCase
    )


class GoHubPokeDetailFactory(Factory[Pokemon]):
    def create(self, url: str):
        scraper = SeleniumHtmlScraper(url)

        with scraper as selenium_scraper:
            raw_html = selenium_scraper.fetch_html()

        soup_adapter = BeautifulSoupHtmlAdapter(raw_html)

        sanitizer = PokeNameSanitizer()
        categorizer = PokemonCategorizer(
            all_keyword_categories,
            sanitizer
        )

        url_generator = PokeApiUrlGenerator()

        poke_detail_use_case = FetchGoHubPokemonDetailUseCase(
            soup_adapter
        )

        pokemon_assembler = PokemonAssembler(
            poke_detail_use_case,
            categorizer,
            url_generator
        )

        return pokemon_assembler.assemble()
