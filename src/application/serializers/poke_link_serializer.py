from src.domain.entities.poke_link import PokeLink


class PokeLinkSerializer:
    @staticmethod
    def serialize(link: PokeLink) -> dict[str, str]:
        return {
            "name": link.name,
            "url": link.url,
        }
