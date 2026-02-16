import wn

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

"""

palavra = "amor"

w_pt = wn.Wordnet(lang="pt", lexicon="own-pt")
w_en = wn.Wordnet(lang="en", lexicon="oewn")
w_de = wn.Wordnet(lang="de", lexicon="odenet")



for s in w_de.synsets("liebe"):
    print("Definition:", s.definition())
    print("Lemmas:", s.lemmas())
    print("-" * 30)


for s in w_pt.synsets("amor"):
    print("Definition:", s.definition())
    print("Lemmas:", s.lemmas())
    print("-" * 30)


for s in w_en.synsets("love"):
    print("Definition:", s.definition())
    print("Lemmas:", s.lemmas())
    print("-" * 30)
"""


import wn

palavra = "less"

def buscar_definicoes_sinonimos(palavra, lang, lexicon):
    w = wn.Wordnet(lang=lang, lexicon=lexicon)
    definicoes = []
    sinonimos = []

    for s in w.synsets(palavra):
        definicoes.append(s.definition() or "")
        sinonimos.extend(s.lemmas())
    return list(set(definicoes)), list(set(sinonimos))

definicoes_pt, sinonimos_pt = buscar_definicoes_sinonimos(palavra, "pt", "omw-pt")
definicoes_en, sinonimos_en = buscar_definicoes_sinonimos(palavra, "en", "oewn")
definicoes_de, sinonimos_de = buscar_definicoes_sinonimos(palavra, "de", "odenet")

print("PT:", definicoes_pt, sinonimos_pt)
print("EN:", definicoes_en, sinonimos_en)
print("DE:", definicoes_de, sinonimos_de)
