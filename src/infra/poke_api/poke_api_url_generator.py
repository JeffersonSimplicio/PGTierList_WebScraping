from src.domain.services.url_generator import UrlGenerator
from src.infra.poke_api.name_formatter import NameFormatter
from src.infra.poke_api.special_case_handler import SpecialCaseHandler
from src.infra.poke_api.variant_name_normalizer import VariantNameNormalizer


class PokeApiUrlGenerator(UrlGenerator):
    BASE_URL = "https://pokeapi.co/api/v2/"

    def __init__(self) -> None:
        self._normalizer = VariantNameNormalizer()
        self._special_handler = SpecialCaseHandler()
        self._formatter = NameFormatter()

    def generate(self, name: str, categories: dict[str, bool]) -> str:
        endpoint_pokeapi = name.lower().strip()

        normalized_name = self._normalizer.normalize(
            endpoint_pokeapi, categories
        )

        special_case_url_part = self._special_handler.handle(
            normalized_name, categories
        )

        if special_case_url_part:
            return self.BASE_URL + "pokemon-form/" + special_case_url_part

        formatted_name = self._formatter.format(normalized_name, categories)

        return self.BASE_URL + "pokemon/" + formatted_name
