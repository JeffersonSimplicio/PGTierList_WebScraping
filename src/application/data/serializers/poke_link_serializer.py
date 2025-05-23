from src.domain.protocols.serializer import Serializer
from src.domain.entities.poke_link import PokeLink


class PokeLinkSerializer(Serializer[PokeLink, str]):
    @staticmethod
    def serialize(poke_link: PokeLink) -> dict[str, str]:
        return {
            "name": poke_link.name,
            "url": poke_link.url,
        }
