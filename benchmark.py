# Jev su MASSIVE 1.1: stesse frasi di test in italiano e in inglese, stesso prompt.
# Salva una riga per frase, quindi se si interrompe basta rilanciarlo.

import json
import random

from typesafe_sdk import Choice, TypeSafeClient

from utils import DATI, ISTRUZIONI, MODELLO, RISULTATI, carica, carica_intenti, giusta

N_FRASI = 2974  # tutto il test set
SEME = 42
LINGUE = ["it-IT", "en-US"]
COSTO_TOKEN = 0.042 / 1_000_000  # $ per token di input

intenti = carica_intenti()

frasi = {}
for lingua in LINGUE:
    frasi[lingua] = {r["id"]: r for r in carica(DATI / f"{lingua}.jsonl") if r["partition"] == "test"}

mancanti = {r["intent"] for f in frasi.values() for r in f.values()} - set(intenti)
assert not mancanti, f"intenti senza descrizione: {mancanti}"

ids = sorted(set(frasi["it-IT"]) & set(frasi["en-US"]), key=int)
random.Random(SEME).shuffle(ids)
ids = ids[:N_FRASI]

RISULTATI.mkdir(exist_ok=True)
domanda = Choice(instructions=ISTRUZIONI, criteria=intenti)

with TypeSafeClient(model=MODELLO) as client:
    for lingua in LINGUE:
        file_out = RISULTATI / f"{lingua}.jsonl"
        fatte = {r["id"] for r in carica(file_out)} if file_out.exists() else set()
        da_fare = [i for i in ids if i not in fatte]
        print(lingua, "- da fare:", len(da_fare))

        with open(file_out, "a", encoding="utf-8") as out:
            for n, i in enumerate(da_fare, 1):
                r = frasi[lingua][i]
                risposta = client.system_one(state={"utterance": r["utt"]}, questions={"intento": domanda})
                a = risposta.answers["intento"]
                riga = {
                    "id": i,
                    "lingua": lingua,
                    "frase": r["utt"],
                    "intento_vero": r["intent"],
                    "intento_jev": a.choice,
                    "confidenza": a.confidence,
                    "probabilita": a.probabilities,
                    "modello": risposta.model,
                    "token_input": risposta.usage.input_tokens,
                }
                out.write(json.dumps(riga, ensure_ascii=False) + "\n")
                out.flush()
                print(n, "ok" if giusta(riga) else "NO", r["utt"])

print()
nel_campione = set(ids)
for lingua in LINGUE:
    righe = [r for r in carica(RISULTATI / f"{lingua}.jsonl") if r["id"] in nel_campione]
    corrette = sum(giusta(r) for r in righe)
    token = sum(r["token_input"] for r in righe)
    print(f"{lingua}: {corrette}/{len(righe)} ({corrette / len(righe):.1%}), costo ~${token * COSTO_TOKEN:.2f}")
