# Grafici per il README, salvati in grafici/

from pathlib import Path

import matplotlib.pyplot as plt

from utils import carica, giusta

CARTELLA = Path("grafici")
CARTELLA.mkdir(exist_ok=True)

it = carica("risultati/it-IT.jsonl")
en = carica("risultati/en-US.jsonl")
it_q = carica("risultati/it-IT-interrogativo.jsonl")
ids_q = {r["id"] for r in it_q}


def errore(righe, ids=None):
    if ids is not None:
        righe = [r for r in righe if r["id"] in ids]
    return 100 * sum(not giusta(r) for r in righe) / len(righe)


# 1. tasso di errore: tutto il test set e solo le domande
fig, (sx, dx) = plt.subplots(1, 2, figsize=(9, 4), sharey=True)

b = sx.bar(["Italian", "English"], [errore(it), errore(en)], color=["C0", "C1"])
sx.bar_label(b, fmt="%.1f%%")
sx.set_title(f"All test utterances (n={len(it):,})")
sx.set_ylabel("Error rate (%)")

b = dx.bar(["Italian\nno \"?\"", "Italian\nwith \"?\"", "English"],
           [errore(it, ids_q), errore(it_q), errore(en, ids_q)], color=["C0", "C2", "C1"])
dx.bar_label(b, fmt="%.1f%%")
dx.set_title(f"Questions only (n={len(ids_q)})")
sx.set_ylim(0, max(errore(it), errore(it, ids_q)) * 1.2)  # spazio per le etichette

fig.tight_layout()
fig.savefig(CARTELLA / "errori.png", dpi=150)
plt.close(fig)


# 2. calibrazione: confidenza media vs accuratezza, fasce da 0.1
fig, ax = plt.subplots(figsize=(5, 5))
ax.plot([0, 1], [0, 1], "--", color="gray", label="perfect calibration")

for nome, righe, colore in [("Italian", it, "C0"), ("English", en, "C1")]:
    xs, ys = [], []
    for k in range(10):
        fascia = [r for r in righe if k / 10 <= r["confidenza"] < (k + 1) / 10 or (k == 9 and r["confidenza"] == 1)]
        if len(fascia) < 20:  # troppo poche frasi per dire qualcosa
            continue
        xs.append(sum(r["confidenza"] for r in fascia) / len(fascia))
        ys.append(sum(giusta(r) for r in fascia) / len(fascia))
    ax.plot(xs, ys, "o-", color=colore, label=nome)

ax.set_xlabel("Declared confidence")
ax.set_ylabel("Actual accuracy")
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.legend()
fig.tight_layout()
fig.savefig(CARTELLA / "calibrazione.png", dpi=150)
plt.close(fig)


# 3. soglie: quante frasi gestisci in automatico e con che accuratezza
fig, ax = plt.subplots(figsize=(6, 4))

for nome, righe, colore in [("Italian", it, "C0"), ("English", en, "C1")]:
    xs, ys = [], []
    for s in [i / 100 for i in range(100)]:
        sopra = [r for r in righe if r["confidenza"] >= s]
        if len(sopra) < 50:
            break
        xs.append(100 * len(sopra) / len(righe))
        ys.append(100 * sum(giusta(r) for r in sopra) / len(sopra))
    ax.plot(xs, ys, color=colore, label=nome)

    sopra = [r for r in righe if r["confidenza"] >= 0.9]
    x09 = 100 * len(sopra) / len(righe)
    y09 = 100 * sum(giusta(r) for r in sopra) / len(sopra)
    ax.plot(x09, y09, "o", color=colore)
    ax.annotate("0.9", (x09, y09), textcoords="offset points", xytext=(5, 5))

ax.set_xlabel("Utterances handled automatically (%)")
ax.set_ylabel("Accuracy on those (%)")
ax.set_title("Moving the confidence threshold")
ax.legend()
fig.tight_layout()
fig.savefig(CARTELLA / "soglie.png", dpi=150)
plt.close(fig)

print("Grafici salvati in", CARTELLA)
