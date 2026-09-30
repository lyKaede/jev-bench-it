from utils import carica, giusta

FASCE = [(0.0, 0.5), (0.5, 0.7), (0.7, 0.9), (0.9, 1.01)]
SOGLIE = [0.5, 0.7, 0.8, 0.9, 0.95]


def accuratezza(righe):
    return sum(giusta(r) for r in righe) / len(righe)


for nome, file in [("IT", "risultati/it-IT.jsonl"), ("EN", "risultati/en-US.jsonl")]:
    righe = carica(file)
    print()
    print(nome)

    print("confidenza dichiarata -> accuratezza reale")
    for basso, alto in FASCE:
        fascia = [r for r in righe if basso <= r["confidenza"] < alto]
        if not fascia:
            continue
        media = sum(r["confidenza"] for r in fascia) / len(fascia)
        print(f"  {basso:.1f}-{min(alto, 1):.1f}: n={len(fascia):4}  conf={media:.2f}  acc={accuratezza(fascia):.2f}")

    print("soglia -> % gestite in automatico, accuratezza")
    for s in SOGLIE:
        sopra = [r for r in righe if r["confidenza"] >= s]
        if sopra:
            print(f"  {s}: {len(sopra) / len(righe):.0%}  {accuratezza(sopra):.1%}")
