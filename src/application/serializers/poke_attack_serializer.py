from src.domain.protocols.serializer_protocol import SerializerProtocol
from src.domain.entities.poke_attack import PokeAttack


class PokeAttackSerializer(SerializerProtocol[PokeAttack, str]):
    @staticmethod
    def serialize(attack: PokeAttack) -> dict[str, str]:
        return {
            "attack_type": attack.attack_type,
            "fast": attack.fast,
            "charged": attack.charged,
        }
