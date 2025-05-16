from src.domain.entities.pokemon import Pokemon
from src.application.serializers.poke_attack_serializer import (
    PokeAttackSerializer,
)


class PokemonSerializer:
    @staticmethod
    def serialize(pokemon: Pokemon) -> dict:
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
