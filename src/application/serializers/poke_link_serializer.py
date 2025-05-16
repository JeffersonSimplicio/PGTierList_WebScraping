from src.domain.protocols.serializer_protocol import SerializerProtocol
from src.domain.entities.poke_link import PokeLink


class PokeLinkSerializer(SerializerProtocol[PokeLink, str]):
    @staticmethod
    def serialize(poke_link: PokeLink) -> dict[str, str]:
        return {
            "name": poke_link.name,
            "url": poke_link.url,
        }
