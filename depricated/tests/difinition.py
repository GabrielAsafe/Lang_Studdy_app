
#python -m wn lexicons #show the installed ones
"""
Lexicon dependencies not available: omw-en:2.0
  w = Wordnet(lang=lang, lexicon=lexicon or "*")
oewn    2025+   [en]    Open English Wordnet
odenet  1.4     [de]    Offenes Deutsches WordNet
own-pt  1.0.0   [pt]    OpenWordnet-PT
own-en  1.0.0   [en]    OpenWordnet-EN
omw-pt  2.0     [pt]    OpenWN-PT

"""
#python -m wn download [own-pt:1.0.0] #download a new one

import wn

# Criar Wordnets
w_en = wn.Wordnet(lang="en", lexicon="oewn")
w_pt = wn.Wordnet(lang="pt", lexicon="own-pt")
w_de = wn.Wordnet(lang="de", lexicon="odenet")

palavra = "love"

def buscar_definicoes_sinonimos(w, palavra):
    definicoes = []
    sinonimos = []
    synsets = w.synsets(palavra)

    for s in synsets:
        if s.definition():
            definicoes.append(s.definition())
        sinonimos.extend([l.format() for l in s.lemmas()])

    return list(set(definicoes)), list(set(sinonimos)), synsets


def buscar_definicoes_traduzidas(synsets, w_target):
    definicoes = []
    for s in synsets:
        if s.ili:
            for s_target in w_target.synsets(ili=s.ili):
                if s_target.definition():
                    definicoes.append(s_target.definition())
    return list(set(definicoes))


# Inglês
def_en, sin_en, synsets_en = buscar_definicoes_sinonimos(w_en, palavra)

# Traduções por conceito
def_pt = buscar_definicoes_traduzidas(synsets_en, w_pt)
def_de = buscar_definicoes_traduzidas(synsets_en, w_de)

# print("EN:", def_en, sin_en)
# print("PT:", def_pt)
# print("DE:", def_de)
