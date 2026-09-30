# Accuratezza sulle frasi dell'esperimento del "?" (senza ?, con ?, inglese)

from utils import carica, giusta

it = carica("risultati/it-IT.jsonl")
en = carica("risultati/en-US.jsonl")
it_q = carica("risultati/it-IT-interrogativo.jsonl")

ids = {r["id"] for r in it_q}
print("Frasi nell'esperimento:", len(ids))

for nome, righe in [("IT senza ?", it), ("IT con ?", it_q), ("EN", en)]:
    corrette = sum(giusta(r) for r in righe if r["id"] in ids)
    print(f"{nome}: {corrette}/{len(ids)} ({corrette / len(ids):.1%})")
