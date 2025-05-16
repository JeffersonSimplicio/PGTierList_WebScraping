from src.domain.protocols.serializer_protocol import SerializerProtocol
from typing import Any
from src.domain.entities.pokemon import Pokemon
from src.application.serializers.poke_attack_serializer import (
    PokeAttackSerializer,
)


class PokemonSerializer(SerializerProtocol[Pokemon, Any]):
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
            "categories": pokemon.categories,
            "url_api": pokemon.api_url,
        }
