from src.domain.entities.pokemon import Pokemon
from src.domain.services.categorization.classifier import Classifier
from src.domain.services.url_generator import UrlGenerator
from src.application.protocols.assembler import Assembler
from src.domain.use_case.fetch_pokemon_detail_use_case import (
    FetchPokemonDetailUseCase
)


class PokemonAssembler(Assembler[Pokemon]):
    def __init__(
        self,
        fetch_details: FetchPokemonDetailUseCase,
        classifier: Classifier,
        url_generator: UrlGenerator
    ):
        self._fetch_details = fetch_details
        self._classifier = classifier
        self._url_generator = url_generator

    def assemble(self) -> Pokemon:
        pokemon_basic_data = self._fetch_details.parse()
        categories = self._classifier.classify(pokemon_basic_data.name)
        url_api = self._url_generator.generate(
            pokemon_basic_data.name, categories
        )
        pokemon_basic_data.categories = categories
        pokemon_basic_data.url_api = url_api
        return pokemon_basic_data
