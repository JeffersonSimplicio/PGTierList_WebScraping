from src.scraping.move_scraper import MoveScraper
from src.scraping.poke_move_scraper import PokeMoveScraper
from src.utilities.json_handler import JsonHandler


class PokeMoveJSON:
    def __init__(
        self,
        scraper: type[MoveScraper],
        poke_move_scraping: type[PokeMoveScraper],
        fast_attacks_pt_br_link: str,
        charge_attacks_pt_br_link: str,
        fast_attacks_en_link: str,
        charge_attacks_en_link: str
    ):
        self.scraper = scraper
        self.poke_move_scraping = poke_move_scraping
        self.fast_attacks_pt_br_link = fast_attacks_pt_br_link
        self.charge_attacks_pt_br_link = charge_attacks_pt_br_link
        self.fast_attacks_en_link = fast_attacks_en_link
        self.charge_attacks_en_link = charge_attacks_en_link

    def generate(self):
        fast_attacks_en = PokeMoveScraper(
            MoveScraper(self.fast_attacks_en_link)
        ).get_move_list()

        fast_attacks_pt_br = PokeMoveScraper(
            MoveScraper(self.fast_attacks_pt_br_link)
        ).get_move_list()

        charge_attacks_en = PokeMoveScraper(
            MoveScraper(self.charge_attacks_en_link)
        ).get_move_list()

        charge_attacks_pt_br = PokeMoveScraper(
            MoveScraper(self.charge_attacks_pt_br_link)
        ).get_move_list()

        fast_attacks = dict(zip(fast_attacks_en, fast_attacks_pt_br))

        charge_attacks = dict(zip(charge_attacks_en, charge_attacks_pt_br))

        attacks = {
            "fast_attacks": fast_attacks,
            "charge_attacks": charge_attacks
        }

        return attacks

    def generate_json(self, file_name: str = "pg_move_list") -> None:
        JsonHandler(file_name).write(self.generate())
