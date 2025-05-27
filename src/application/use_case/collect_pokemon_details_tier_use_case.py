from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.domain.entities.pokemon import Pokemon
from src.domain.entities.poke_link import PokeLink
from src.application.protocols.factory import Factory
from src.application.protocols.collect_pokemon_details_tier import (
    CollectPokemonDetailsByTier
)


class CollectPokemonDetailsByTierUseCase(
    CollectPokemonDetailsByTier
):
    def __init__(
        self,
        tiered_links: Factory[dict[str, list[PokeLink]]],
        details_factory: Factory[Pokemon],
        url: Optional[str] = None,
    ):
        self._tiered_links = (
            tiered_links.create(url) if url else tiered_links.create()
        )
        self._details_factory = details_factory

    def execute(self):
        result: dict[str, list[Pokemon]] = {}

        with ThreadPoolExecutor(max_workers=10) as executor:
            for tier, poke_links in self._tiered_links.items():
                future_to_index = {
                    executor.submit(
                        self._details_factory.create,
                        link.url
                    ): idx
                    for idx, link in enumerate(poke_links)
                }

                ordered_pokemons: list[Optional[Pokemon]] = (
                    [None] * len(poke_links)
                )

                for future in as_completed(future_to_index):
                    idx = future_to_index[future]
                    try:
                        pokemon = future.result()
                        ordered_pokemons[idx] = pokemon
                    except Exception as e:
                        print(
                            f"Erro ao buscar detalhes para índice {idx} "
                            f"no tier {tier}: {e}"
                        )

                result[tier] = [p for p in ordered_pokemons if p is not None]

        return result
