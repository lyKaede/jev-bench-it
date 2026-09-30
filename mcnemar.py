# Test di McNemar esatto sulle coppie discordanti (giusta in un caso e sbagliata nell'altro).
# Se le due condizioni fossero equivalenti, le discordanti si dividerebbero a metà.

from math import comb

from utils import carica, giusta


def p_value(b, c):
    n = b + c
    k = min(b, c)
    p = 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(p, 1.0)


def per_id(file):
    return {r["id"]: giusta(r) for r in carica(file)}


def confronta(titolo, a, b, nome_a, nome_b):
    ids = [i for i in b if i in a]
    solo_a = sum(1 for i in ids if a[i] and not b[i])
    solo_b = sum(1 for i in ids if b[i] and not a[i])
    print()
    print(f"{titolo} (n={len(ids)})")
    print(f"  giuste solo {nome_a}: {solo_a}, solo {nome_b}: {solo_b}, p = {p_value(solo_a, solo_b):.2g}")


it = per_id("risultati/it-IT.jsonl")
en = per_id("risultati/en-US.jsonl")
it_q = per_id("risultati/it-IT-interrogativo.jsonl")

confronta("IT vs EN, tutto il test set", en, it, "EN", "IT")
confronta("IT con ? vs senza ?, sulle domande", it_q, it, "con ?", "senza ?")
confronta("IT con ? vs EN, sulle domande", en, it_q, "EN", "IT con ?")
