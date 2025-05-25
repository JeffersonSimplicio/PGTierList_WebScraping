from typing import Any
from src.domain.entities.poke_attack import PokeAttack
from src.domain.services.html_adapter import HtmlAdapter


class GoHubAttackExtractor:
    def __init__(self, html_adapter: HtmlAdapter, ):
        self._html_adapter = html_adapter

    def extract(self, types: list[str]) -> list[PokeAttack]:
        tmp_types = types.copy()
        table_body = self._html_adapter.select(
            "table.DataGrid_dataGrid__Q3gQi tbody"
        )

        if table_body is None:
            return []

        attacks = []
        for tr in table_body:
            type_fast_attack = self._get_attack_type(tr, 2)
            type_charged_attack = self._get_attack_type(tr, 3)

            if type_fast_attack == type_charged_attack:
                try:
                    tmp_types.remove(type_charged_attack)

                    fast_attack = self._get_attack_name(tr, 2)
                    charged_attack = self._get_attack_name(tr, 3)

                    attacks.append(
                        PokeAttack(
                            type_charged_attack,
                            fast_attack,
                            charged_attack
                        )
                    )
                    if len(types) == 0:
                        break
                except ValueError:
                    continue

        if len(attacks) == 0:
            tr = self._html_adapter.select_one(table_body, "tr:first-child")
            if tr:
                type_charged_attack = self._get_attack_type(tr, 3)
                fast_attack = self._get_attack_name(tr, 2)
                charged_attack = self._get_attack_name(tr, 3)
                attacks.append(
                    PokeAttack(
                        type_charged_attack,
                        fast_attack,
                        charged_attack
                    )
                )
        return attacks

    def _get_attack_type(self, tr: Any, index: int) -> str:
        td_element = self._html_adapter.select(
            f"td:nth-child({index}) a",
            in_element=tr
        )
        img = self._html_adapter.select(
            "img",
            in_element=td_element
        )
        return self._html_adapter.get_attr("title", in_element=img).strip()

    def _get_attack_name(self, tr: Any, index: int) -> str:
        td_element = self._html_adapter.select(
            f"td:nth-child({index}) a",
            in_element=tr
        )
        return self._html_adapter.get_text(td_element)
