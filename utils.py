import json
from pathlib import Path

MODELLO = "jev-1.13.0"
ISTRUZIONI = (
    "The user is talking to a smart home voice assistant called Olly. "
    "Which action does the user want the assistant to perform?"
)

DATI = Path("1.1/data")
RISULTATI = Path("risultati")


def carica(percorso):
    with open(percorso, encoding="utf-8") as f:
        return [json.loads(riga) for riga in f if riga.strip()]


def carica_intenti():
    return json.loads(Path("intenti.json").read_text(encoding="utf-8"))


def giusta(r):
    return r["intento_vero"] == r["intento_jev"]
