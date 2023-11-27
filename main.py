import sys
from time import time
from src.utilities.Terminal import Terminal
from src.PokeRankingJSON import PokeRankingJSON
from src.Security import SecurityManager


start = time()

password = sys.argv[1]  # "senha_difícil" - IndexError:

TIER_LIST_LINK = "/pokemongo/attackers-tier-list#topic-281631"

HASH = b'$2b$12$4y3u4JJNrPm3cccAX.Ema.GRTYKdPSlQL340yFFBaYkBkbEnsaRzC'

authorized = SecurityManager.compare(password, HASH)

instance: PokeRankingJSON

if authorized:
    instance = PokeRankingJSON(TIER_LIST_LINK)
    instance.generate_json()

end = time()

execution_time = start - end
Terminal.clear()
poke_number = instance.number_pokemon()
print(f"{poke_number}/{poke_number}")
print("Operação concluída!")
print(f"Tempo decorrido: {(execution_time/60):.2f} minutos")
