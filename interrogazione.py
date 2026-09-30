# Esperimento: aggiungo "?" alle frasi italiane che in inglese sono domande
# e rifaccio girare Jev solo su quelle. La regola guarda solo la frase inglese,
# mai l'etichetta, altrimenti il "?" darebbe un indizio sulla risposta.

import json
from pathlib import Path

from typesafe_sdk import Choice, TypeSafeClient

from utils import ISTRUZIONI, MODELLO, carica, carica_intenti

PAROLE_DOMANDA = {
    "do", "does", "did", "is", "are", "was", "were", "am",
    "can", "could", "will", "would", "should", "shall",
    "have", "has", "what", "where", "when", "who", "whose",
    "which", "why", "how",
}


def e_domanda(frase_en):
    parole = frase_en.lower().split()
    if parole and parole[0] == "olly":  # nome dell'assistente
        parole = parole[1:]
    return len(parole) > 0 and parole[0] in PAROLE_DOMANDA


it = carica("risultati/it-IT.jsonl")
en_per_id = {r["id"]: r for r in carica("risultati/en-US.jsonl")}

domande = [r for r in it if e_domanda(en_per_id[r["id"]]["frase"])]
print("Frasi con il ?:", len(domande))

# prompt identico al benchmark (preso da utils), cambia solo il "?"
domanda = Choice(instructions=ISTRUZIONI, criteria=carica_intenti())

file_out = Path("risultati/it-IT-interrogativo.jsonl")
fatte = {r["id"] for r in carica(file_out)} if file_out.exists() else set()

with TypeSafeClient(model=MODELLO) as client, open(file_out, "a", encoding="utf-8") as out:
    for n, r in enumerate(domande, 1):
        if r["id"] in fatte:
            continue
        frase = r["frase"] + "?"
        risposta = client.system_one(state={"utterance": frase}, questions={"intento": domanda})
        a = risposta.answers["intento"]
        riga = {
            "id": r["id"],
            "frase": frase,
            "intento_vero": r["intento_vero"],
            "intento_jev": a.choice,
            "confidenza": a.confidence,
        }
        out.write(json.dumps(riga, ensure_ascii=False) + "\n")
        out.flush()
        print(f"{n}/{len(domande)}", frase)
