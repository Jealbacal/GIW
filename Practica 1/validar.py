automata_ok = {
    "alfabeto": {0, 1},
    "estados": {"p", "q", "r"},
    "inicial": "p",
    "finales": {"q"},
    "transicion": {
        ("p", "0"): "q",
        ("p", "1"): "r",
        ("q", "0"): "r",
        ("q", "1"): "q",
        ("r", "0"): "r",
        ("r", "1"): "r",
    },
}

automata_mal1 = {
    "alfabeto": {0, 1},
    "estados": {"p", "q", "r"},
    "inicial": "p",
    "finales": {"q"},
    "transicion": {
        ("p", "0"): "q",
        ("p", "1"): "r",
        ("q", "0"): "r",
        ("q", "1"): "q",
        ("r", "0"): "r",
        ("r", "1"): "r",
    },
}


def validarF(automata):
    estados = automata.get("estados")
    finales = automata.get("finales")
    for estado in finales:
        if estado not in estados:
            return False

    return True


def validarT(automata):
    trans = automata.get("transicion")
    estados = tuple(automata.get("estados"))
    alf = tuple(automata.get("alfabeto"))
    result = True

    for clave in trans:
        if not (
            (trans.get(clave) in estados)
            and (clave[0] in estados)
            and (int(clave[1]) in alf)
        ):
            result = False

    return result and (len(trans) == len(estados) * len(alf))


def validar(automata):
    return (
        automata.get("alfabeto") is not None
        and len(automata) == 5
        and automata.get("estados") is not None
        and automata.get("inicial") in automata.get("estados")
        and validarF(automata)
        and validarT(automata)
    )


print(validar(automata_mal1))



######
# quedaria 2.2 2.3 y leer los automatas