import requests
from bs4 import BeautifulSoup


class PokeInfoScraping:
    def __init__(self, link: str) -> None:
        self._GAMEPRESS_LINK = link

        page = requests.get(self._GAMEPRESS_LINK)
        html_content = page.text
        self._soup = BeautifulSoup(html_content, "html.parser")

    def a_level_lines(self):
        pve_table = self._soup.select_one(
            "div.pve-section-new table.moveset-table tbody"
        )

        level_a = []
        if pve_table is not None:
            list_trs = pve_table.find_all("tr")
            for line in list_trs:
                attack_note_cell = line.select_one(
                    "td:nth-child(3) div.grade-881"
                )
                if attack_note_cell is not None:
                    level_a.append(attack_note_cell)

        level_a_attack_lines = [attack.parent.parent for attack in level_a]

        td_set = []
        for attack_line in level_a_attack_lines:
            td = attack_line.find_all(recursive=False)[:2]
            td_set.append(td)

        return td_set

    def attacks_types_dict(self) -> dict[str, list[str]]:
        td_set = self.a_level_lines()
        type_attack_list = {}

        for column in td_set:
            attacks = []
            for cell in column:
                attack = cell.find("div", class_="move-name").string.strip()
                attacks.append(attack)

            type_ = column[1]\
                .find("img")\
                .get("src")\
                .split('_')[0]\
                .split('/')[-1]\
                .lower()

            if type_ not in type_attack_list:
                type_attack_list[type_] = [attacks]
            else:
                type_attack_list[type_].append(attacks)

        return type_attack_list

    def get_poke_types(self) -> list[str]:
        div_types_classes = (
            ".field" +
            ".field--name-field-pokemon-type" +
            ".field--type-entity-reference" +
            ".field--label-hidden" +
            ".field__items"
        )
        div_name_types = (
            ".field" +
            ".field--name-name" +
            ".field--type-string" +
            ".field--label-hidden" +
            ".field__item"
        )
        list_types = self._soup.select(
            f"div{div_types_classes} div{div_name_types}"
        )
        y = [type_.string for type_ in list_types]
        return y

    def run(self):
        return self.attacks_types_dict()


if __name__ == "__main__":
    GAMEPRESS_LINK = "https://gamepress.gg"
    POKE_INFO_LINK = "/pokemongo/pokemon/384-mega"
    # POKE_INFO_LINK = "/pokemongo/pokemon/373-shadow"
    # POKE_INFO_LINK = "/pokemongo/pokemon/142-shadow"
    # POKE_INFO_LINK = "/pokemongo/pokemon/465-shadow"

    xyz = PokeInfoScraping(GAMEPRESS_LINK+POKE_INFO_LINK)
    a = xyz.run()
    print(a)
