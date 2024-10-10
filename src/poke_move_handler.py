from src.scraping.move_scraper import MoveScraper
from src.scraping.poke_move_scraper import PokeMoveScraper
from src.poke_move_JSON import PokeMoveJSON

FAST_ATTACKS_PT_BR = "https://db.pokemongohub.net/pt/moves-list/category-fast"
CHARGE_ATTACKS_PT_BR = (
    "https://db.pokemongohub.net/pt/moves-list/category-charge"
)
FAST_ATTACKS_EN = "https://db.pokemongohub.net/moves-list/category-fast"
CHARGE_ATTACKS_EN = "https://db.pokemongohub.net/moves-list/category-charge"


class PokeMoveHandler:
    def run(self):
        moves = PokeMoveJSON(
            MoveScraper,
            PokeMoveScraper,
            FAST_ATTACKS_PT_BR,
            CHARGE_ATTACKS_PT_BR,
            FAST_ATTACKS_EN,
            CHARGE_ATTACKS_EN
        )
        moves.generate_json()
