from src.domain.entities.poke_attack import PokeAttack


class PokeAttackSerializer:
    @staticmethod
    def serialize(attack: PokeAttack) -> dict[str, str]:
        return {
            "attack_type": attack.attack_type,
            "fast": attack.fast,
            "charged": attack.charged,
        }
