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
