from src.domain.entities.pokemon import Pokemon
from src.domain.services.categorization.classifier import Classifier
from src.domain.services.url_generator import UrlGenerator
from src.application.protocols.assembler import Assembler


class PokemonAssembler(Assembler[Pokemon]):
    def __init__(
        self,
        pokemon: Pokemon,
        classifier: Classifier,
        url_generator: UrlGenerator
    ):
        self._pokemon_basic_data = pokemon
        self._classifier = classifier
        self._url_generator = url_generator

    def assemble(self) -> Pokemon:
        categories = self._classifier.classify(self._pokemon_basic_data.name)
        url_api = self._url_generator.generate(
            self._pokemon_basic_data.name, categories
        )
        self._pokemon_basic_data.categories = categories
        self._pokemon_basic_data.url_api = url_api
        return self._pokemon_basic_data
