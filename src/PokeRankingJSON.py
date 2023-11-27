import json
from src.utilities.Terminal import Terminal
from src.PokemonModel import Pokémon
from src.scraping.PokeInfoScraping import PokeInfoScraping
from src.scraping.TierListScraping import TierListScraping


class PokeRankingJSON:
    def __init__(self, tier_list_link) -> None:
        self.tier_list_link = tier_list_link

        self.GAMEPRESS_LINK = "https://gamepress.gg"
        self.tier_list = TierListScraping(
            self.GAMEPRESS_LINK+self.tier_list_link
        )

    def number_pokemon(self):
        return self.tier_list.number_pokemon()

    def generate_ranking(self) -> dict[str, dict[str, list[dict[str, any]]]]:
        poke_ranking = dict()
        real_tier_list = self.tier_list.run()
        number_pokemon = self.tier_list.number_pokemon()
        count = 0

        for key, value in real_tier_list.items():
            rank = "_".join(key.split()).lower()
            for poke in value:
                count += 1
                poke_name = poke["name"]
                poke_link = poke["link"]
                # Terminal
                Terminal.clear()
                print(f"{count}/{number_pokemon}")
                print(f"{((count / number_pokemon) * 100):.2f}%")
                print(f"Pokemon atual: {poke_name}")

                info_poke = PokeInfoScraping(self.GAMEPRESS_LINK+poke_link)
                datas = info_poke.run()

                poke_info: dict[str, any]
                if len(datas) != 0:
                    for type_, attacks in datas.items():
                        quick_attack = []
                        charged_attack = []
                        for attack in attacks:
                            quick_attack.append(attack[0])
                            charged_attack.append(attack[1])
                        x = Pokémon(
                            poke_name,
                            type_,
                            quick_attack,
                            charged_attack
                        )
                        poke_info = x.generate()
                else:
                    poke_type = info_poke.get_poke_types()
                    x = Pokémon(
                        poke_name,
                        poke_type,
                        [],
                        []
                    )
                    poke_info = x.generate()

                if type_ in poke_ranking:
                    if rank in poke_ranking[type_]:
                        poke_ranking[type_][rank].append(poke_info)
                    else:
                        poke_ranking[type_][rank] = [poke_info]
                else:
                    poke_ranking[type_] = {rank: [poke_info]}

        return poke_ranking

    def generate_json(
        self,
        file_name: str = "pg_tier_list",
        data=""
    ) -> None:
        if data == "":
            ranking = self.generate_ranking()
        else:
            ranking = data

        if not file_name.endswith(".json"):
            file_name = file_name+".json"

        with open(file_name, 'w') as file:
            json.dump(ranking, file)
