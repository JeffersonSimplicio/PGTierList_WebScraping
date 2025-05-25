from typing import Callable
from src.domain.services.html_adapter import HtmlAdapter
from src.domain.entities.pokemon import Pokemon
from src.domain.entities.poke_attack import PokeAttack
from src.domain.use_case.fetch_pokemon_detail_use_case import (
    FetchPokemonDetailUseCase
)
from src.infra.use_case.fetch_gohub_pokemon_detail.\
    gohub_attack_extractor import (GoHubAttackExtractor)


class FetchGoHubPokemonDetailUseCase(FetchPokemonDetailUseCase):
    def __init__(
        self,
        html_adapter: HtmlAdapter,
        pokemon_factory: Callable[
            [
                int,
                str,
                list[str],
                list[PokeAttack],
                bool,
                dict[str, bool],
                str,
            ],
            Pokemon,
        ],
    ) -> None:
        self._html_adapter = html_adapter
        self._pokemon_factory = pokemon_factory
        self._attack_extractor = GoHubAttackExtractor(html_adapter)

    def parse(self) -> Pokemon:
        return self._generate_pokemon()

    def _generate_pokemon(self) -> Pokemon:
        name = self._extract_name()
        types = self._extract_types()

        return self._pokemon_factory(
            id=self._extract_id(),
            name=name,
            types=types,
            attacks=self._extract_attacks(types),
            is_shiny_available=self._extract_shiny(),
        )

    def _extract_id(self) -> int:
        pokedex_th = self._html_adapter.find(
            "th",
            string="Pokédex Number"
        )
        td = self._html_adapter.find_next_sibling(
            "td",
            in_element=pokedex_th
        )
        poke_id = self._html_adapter.get_text(td).replace("#", "")
        return int(poke_id)

    def _extract_name(self) -> str:
        h1_element = self._html_adapter.find(
            id="overview-and-stats",
        )
        return self._html_adapter.get_text(h1_element)

    def _extract_types(self) -> list[str]:
        typing_span = self._html_adapter.find(
            "span",
            class_="PokemonPageRenderers_officialImageTyping__BZQBp"
        )
        titles = []
        for img in self._html_adapter.find_all(
            "img",
            recursive=False,
            in_element=typing_span,
        ):
            title = self._html_adapter.get_attr("title", in_element=img)
            titles.append(title)
        return titles

    def _extract_attacks(self, types: list[str]) -> list[PokeAttack]:
        return self._attack_extractor.extract(types)

    def _extract_shiny(self) -> bool:
        shiny_element = self._html_adapter.find_all(
            "span", class_="PokemonPageRenderers_ornamentIcon__ffCq5"
        )
        return len(shiny_element) == 2
