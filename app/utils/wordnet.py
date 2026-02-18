import wn 
ILI_CACHE = {}


def buscar_definicoes_sinonimos(synsets):
    synsets = set(synsets)
    definicoes = [s.definition() for s in synsets if s.definition()]
    sinonimos = [l for s in synsets for l in s.lemmas()]
    return list(set(definicoes)), list(set(sinonimos))



def buscar_definicoes_traduzidas(synsets, w_target, lang):
    definicoes = set()
    palavras = set()

    for s in synsets:
        if not s.ili:
            continue

        for s_target in get_synsets_by_ili(w_target, s.ili, lang):
            if s_target.definition():
                definicoes.add(s_target.definition())

            palavras.update([l for l in s_target.lemmas()])

    return list(definicoes), list(palavras)



def get_synsets_by_ili(w_target, ili, lang):
    key = (lang, ili)  # usa o idioma explicitamente

    if key not in ILI_CACHE:
        ILI_CACHE[key] = w_target.synsets(ili=ili)

    return ILI_CACHE[key]
