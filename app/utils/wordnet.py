import wn 

def buscar_definicoes_sinonimos(synsets):
    """Extrai definições e sinônimos de uma lista de synsets"""
    definicoes = [s.definition() for s in synsets if s.definition()]
    sinonimos = [l for s in synsets for l in s.lemmas()]
    return list(set(definicoes)), list(set(sinonimos))

def buscar_definicoes_traduzidas(synsets, w_target):
    """Dada uma lista de synsets, busca definições no idioma alvo via ILI"""
    definicoes = []
    for s in synsets:
        if s.ili:
            for s_target in w_target.synsets(ili=s.ili):
                if s_target.definition():
                    definicoes.append(s_target.definition())
    return list(set(definicoes))