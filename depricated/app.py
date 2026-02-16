# from flask import Flask, render_template, request, jsonify
# import phunspell #é um corretor ortográfico, analisador morfológico e biblioteca de código aberto projetado para idiomas com morfologia complexa, composto de palavras e suporte Unicode.
# import re
# import wn # WordNet is an English dictionary which is a part of Natural Language Tool Kit (NLTK) for Python.
# import pyttsx3 #text-to-speech conversion.
# from threading import Thread
# import json
# import os



# def buscar_definicoes_sinonimos(synsets):
#     """Extrai definições e sinônimos de uma lista de synsets"""
#     definicoes = [s.definition() for s in synsets if s.definition()]
#     sinonimos = [l for s in synsets for l in s.lemmas()]
#     return list(set(definicoes)), list(set(sinonimos))

# def buscar_definicoes_traduzidas(synsets, w_target):
#     """Dada uma lista de synsets, busca definições no idioma alvo via ILI"""
#     definicoes = []
#     for s in synsets:
#         if s.ili:
#             for s_target in w_target.synsets(ili=s.ili):
#                 if s_target.definition():
#                     definicoes.append(s_target.definition())
#     return list(set(definicoes))

# def speak_text(text):
#     engine.say(text)
#     engine.runAndWait()


# def highlight_texto(texto):
#     """Coloca cada palavra dentro de <span class="palavra">"""
#     def replacer(match):
#         palavra = match.group(0)
#         return f'<span class="palavra" data-palavra="{palavra}">{palavra}</span>'
#     return re.sub(r'\b\w+[.,;:!?]?\b', replacer, texto.replace("\n", "<br>\n"))


# def clean_word(palavra):
#     return re.sub(r"[^\w]", "", palavra)



# def load_config_from_json(app, path="conf.json"):
#     with open(path) as f:
#         config_doc = json.load(f)

#     for item in config_doc["configurations"]:
#         key = item["key"]
#         value = os.getenv(key, item.get("default"))

#         if item.get("required") and value is None:
#             raise RuntimeError(f"Config obrigatória ausente: {key}")

#         app.config[key] = value





# app = Flask(__name__)

# load_config_from_json(app)

# h = phunspell.Phunspell(app.config["TARGET_LANGUAGE"])

# engine = pyttsx3.init()

# # configs fixas
# app.config.update({
#     "LANG": "pt",
#     "LEXICON": "omw-pt",
#     "LANGEN": "en",
#     "LEXICONEN": "oewn",
#     "LANGDE": "de",
#     "LEXICONDE": "odenet"
# })


# @app.route("/", methods=["GET", "POST"])
# def index():
#     texto = ""

#     # Aqui você poderia receber texto do usuário
#     # Por enquanto, vamos usar texto fixo
#     texto = """Todas as cartas de amor são Ridículas.
# Não seriam cartas de amor se não fossem Ridículas.
# Também escrevi em meu tempo cartas de amor, Como as outras,"""

#     # Destaca cada palavra com span
#     texto_span = highlight_texto(texto)

#     return render_template("index.html", texto=texto_span)


# @app.route("/verificar", methods=["POST"])
# def verificar():
#     data = request.json
#     palavra = data.get("palavra", "")
#     sugestoes = []

#     if not palavra:
#         return jsonify({"erro": "nenhuma palavra enviada"}), 400

#     if h.lookup(palavra):
#         return jsonify({"correta": True, "palavra": palavra, "sugestoes": []})
#     else:
#         for sug in h.suggest(palavra):
#             sugestoes.append(sug)
#         return jsonify({"correta": False, "palavra": palavra, "sugestoes": sugestoes[:5]})


# @app.route("/definitions", methods=["POST"])
# def fetch():
#     data = request.json
#     palavra = data.get("palavra", "")
#     lang = data.get("lang", "en_US")  # padrão em inglês

#     # Inicializa Wordnets
#     w_en = wn.Wordnet(lang=app.config["LANGEN"], lexicon=app.config["LEXICONEN"])
#     w_pt = wn.Wordnet(lang=app.config["LANG"], lexicon=app.config["LEXICON"])
#     w_de = wn.Wordnet(lang=app.config["LANGDE"], lexicon=app.config["LEXICONDE"])

#     # Busca synsets em inglês (ponto de partida)
#     synsets_en = w_en.synsets(palavra)
#     definicoes_en, sinonimos = buscar_definicoes_sinonimos(synsets_en)

#     # Traduz para PT e DE via ILI
#     definicoes_pt = buscar_definicoes_traduzidas(synsets_en, w_pt)
#     definicoes_de = buscar_definicoes_traduzidas(synsets_en, w_de)

#     return jsonify({
#         "palavra": palavra,
#         "definicoes": definicoes_pt,
#         "definicoesEN": definicoes_en,
#         "definicoes_de": definicoes_de,
#         "sinonimos": list(set(sinonimos))
#     })


# @app.route("/ler", methods=["POST"])
# def ler():
#     data = request.json
#     palavra = data.get("palavra", "")
#     if not palavra:
#         return jsonify({"error": "Palavra não fornecida"}), 400

#     # Speak in a background thread
#     Thread(target=speak_text, args=(palavra,)).start()

#     return jsonify({"status": "sucesso"})


# @app.route("/clicou", methods=["POST"])
# def clicou():
#     #palavra = request.json["palavra"]
#     #print("Usuário clicou:", palavra)
#     return "", 204


# if __name__ == "__main__":

#     engine.setProperty("rate", 125)
#     engine.setProperty("volume", 1.0)

#     voices = engine.getProperty("voices")
#     engine.setProperty("voice", voices[1].id)

#     app.run(debug=False, threaded=False)