from flask import render_template, request, jsonify, current_app
from threading import Thread
from .utils.tts import speak_text
from .utils.wordnet import buscar_definicoes_sinonimos, buscar_definicoes_traduzidas
import json
import os


def register_routes(app):

    @app.route("/", methods=["GET", "POST"])
    def index():
        return render_template("index.html")


    @app.route("/verificar", methods=["POST"])
    def verificar():
        h = current_app.hunspell  

        data = request.json
        palavra = data.get("palavra", "")
        sugestoes = []

        if not palavra:
            return jsonify({"erro": "nenhuma palavra enviada"}), 400

        if h.lookup(palavra):
            return jsonify({"correta": True, "palavra": palavra, "sugestoes": []})
        else:
            for sug in h.suggest(palavra):
                sugestoes.append(sug)
            return jsonify({"correta": False, "palavra": palavra, "sugestoes": sugestoes[:5]})


    @app.route("/definitions", methods=["POST"])
    def fetch():
        data = request.json
        palavra = data.get("palavra", "")
        lang = data.get("lang", "en_US")  # padrão em inglês
        
        
        # Inicializa Wordnets
        w_en = current_app.wn_en
        w_pt = current_app.wn_pt
        w_de = current_app.wn_de

        
        # Busca synsets em inglês (ponto de partida)
        synsets_en = w_en.synsets(palavra)
        definicoes_en, sinonimos = buscar_definicoes_sinonimos(synsets_en)

        # Traduz para PT e DE via ILI
        definicoes_pt = buscar_definicoes_traduzidas(synsets_en, w_pt)
        definicoes_de = buscar_definicoes_traduzidas(synsets_en, w_de)

        return jsonify({
            "palavra": palavra,
            "definicoes": definicoes_pt,
            "definicoesEN": definicoes_en,
            "definicoes_de": definicoes_de,
            "sinonimos": list(set(sinonimos))
        })


    @app.route("/ler", methods=["POST"])
    def ler():
        palavra = request.json.get("palavra", "")
        engine = current_app.tts_engine
        Thread(target=speak_text, args=(palavra, engine)).start()
        return jsonify({"status": "sucesso"})



    @app.route("/clicou", methods=["POST"])
    def clicou():
        #palavra = request.json["palavra"]
        #print("Usuário clicou:", palavra)
        return "", 204

    @app.route("/update-config", methods=["POST"])
    def update_config():
        data = request.json

        config_path = os.path.join(current_app.root_path, "static", "conf.json")

        with open(config_path, "r") as f:
            config = json.load(f)

        for item in config["configurations"]:
            if item["key"] == "TARGET_LANGUAGE":
                item["default"] = data["TARGET_LANGUAGE"]
            if item["key"] == "BASE_LANGUAGE":
                item["default"] = data["BASE_LANGUAGE"]

        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        return jsonify({"status": "success"})
