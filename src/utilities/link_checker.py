from requests import get
from src.utilities.json_handler import JsonHandler
from src.utilities.terminal import Terminal


class LinkChecker:

    def __init__(self, url_file: str = "pg_tier_list.json"):
        self.url_data = JsonHandler(url_file).read()
        self.broken_links = []

    def check_links(self):
        for tier, poke_list in self.url_data.items():
            print(f"Tier atual: {tier}")
            for poke_info in poke_list:
                poke_name = poke_info["name"]
                poke_link = poke_info["poke_api"]
                print(f"Pokemon em analise: {poke_name}")
                print(f"Link do Pokemon em analise: {poke_link}")

                response = get(poke_link)
                if response.status_code != 200:
                    self.broken_links.append(f"{poke_name} - {poke_link}")
                    Terminal.error(f"O Pokemon {poke_name}, tá com problema.")
                print("-- " * 50)
            print("## " * 50)

    def save_broken_links(self, file_name: str = "broken_links.txt"):
        self.check_links()

        with open(file_name, "w") as f:
            for link in self.broken_links:
                f.write(link + "\n")
        Terminal.success(f"Links problemáticos salvos em: {file_name}")


# Exemplo de uso
if __name__ == "__main__":
    checker = LinkChecker()
    checker.save_broken_links()
