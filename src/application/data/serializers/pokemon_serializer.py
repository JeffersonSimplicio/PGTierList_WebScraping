from typing import Any
from src.domain.entities.pokemon import Pokemon
from src.domain.protocols.serializer import Serializer
from src.application.data.serializers.poke_attack_serializer import (
    PokeAttackSerializer
)


class PokemonSerializer(Serializer[Pokemon, Any]):
    @staticmethod
    def serialize(pokemon: Pokemon) -> dict[str, Any]:
        return {
            "id": pokemon.id,
            "name": pokemon.name,
            "types": pokemon.types,
            "attacks": [
                PokeAttackSerializer.serialize(attack)
                for attack in pokemon.attacks
            ],
            "is_shiny_available": pokemon.is_shiny_available,
            # "categories": pokemon.categories,
            "categories": {
                "is_mega": pokemon.is_in_category("is_mega"),
                "is_primal": pokemon.is_in_category("is_primal"),
                "is_shadow": pokemon.is_in_category("is_shadow"),
            },
            "url_api": pokemon.url_api,
        }
