from utils import carica, giusta

it = carica("risultati/it-IT.jsonl")
en = carica("risultati/en-US.jsonl")

giuste_it = {}
for r in it:
    giuste_it[r["id"]] = giusta(r)

giuste_en = {}
for r in en:
    giuste_en[r["id"]] = giusta(r)

print("Frasi:", len(it))
print("Giuste IT:", sum(giuste_it.values()))
print("Giuste EN:", sum(giuste_en.values()))

# confronto a coppie: le frasi utili sono quelle giuste in una lingua sola
entrambe_giuste = 0
entrambe_sbagliate = 0
solo_en = 0
solo_it = 0

for i in giuste_it:
    if giuste_it[i] and giuste_en[i]:
        entrambe_giuste += 1
    elif giuste_en[i]:
        solo_en += 1
    elif giuste_it[i]:
        solo_it += 1
    else:
        entrambe_sbagliate += 1

print()
print("Entrambe giuste:", entrambe_giuste)
print("Entrambe sbagliate:", entrambe_sbagliate)
print("Solo EN giusta:", solo_en)
print("Solo IT giusta:", solo_it)

# un po' di esempi da leggere a mano
it_per_id = {r["id"]: r for r in it}
en_per_id = {r["id"]: r for r in en}

print()
print("--- giuste in inglese, sbagliate in italiano ---")
mostrate = 0
for i in giuste_it:
    if giuste_en[i] and not giuste_it[i]:
        r = it_per_id[i]
        print()
        print("IT: ", r["frase"])
        print("EN: ", en_per_id[i]["frase"])
        print("vero:", r["intento_vero"], "| jev:", r["intento_jev"], f"({r['confidenza']})")
        mostrate += 1
        if mostrate == 20:
            break


# errori del tipo "domanda letta come azione", es. calendar_query -> calendar_set
def argomento(intento):
    return intento.split("_")[0]


def domanda_scambiata(r):
    vero = r["intento_vero"]
    jev = r["intento_jev"]
    return "query" in vero and "query" not in jev and argomento(vero) == argomento(jev)


print()
for nome, righe in [("IT", it), ("EN", en)]:
    errori = [r for r in righe if not giusta(r)]
    scambiate = [r for r in errori if domanda_scambiata(r)]
    print(f"{nome}: {len(errori)} errori, di cui {len(scambiate)} domande lette come azioni")
