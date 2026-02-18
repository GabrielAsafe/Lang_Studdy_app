from flask import render_template, request, jsonify, current_app
from threading import Thread
from .utils.tts import speak_text
from .utils.parse import gerar_html_completo
from .utils.wordnet import buscar_definicoes_sinonimos, buscar_definicoes_traduzidas
from .utils.pdf import ler_pdf
from .utils.dic import searchEntry


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
        
        print("RETORNANDO JSON verificar:", {
            "palavra": palavra
        })


        if h.lookup(palavra):
            return jsonify({"correta": True, "palavra": palavra, "sugestoes": []})
        else:
            for sug in h.suggest(palavra):
                sugestoes.append(sug)
            return jsonify({"correta": False, "palavra": palavra, "sugestoes": sugestoes[:5]})

    @app.route("/definitions", methods=["POST"])
    def fetch():
        WORDNETS = {
        "en_US": current_app.wn_en,
        "pt_BR": current_app.wn_pt,
        "de_DE": current_app.wn_de
        }
        data = request.json
        palavra = data.get("palavra", "").strip()

        if not palavra:
            return jsonify({"error": "Palavra não fornecida"}), 400

        # Idiomas configurados
        base_lang = app.config['BASE_LANGUAGE']
        target_lang = app.config['TARGET_LANGUAGE']

        # WordNets correspondentes
        w_base = WORDNETS[base_lang]
        w_target = WORDNETS[target_lang]

        # Sinsets base
        synsets_target = w_target.synsets(palavra)


        if not synsets_target:
            return jsonify({
                "erro": "synsets_target estava vazio",
                "palavra": palavra,
                "definicoes_base": [],
                "definicoes_target": [],
                "sinonimos": []
            })


        # Definições e sinónimos na língua base
        definicoes_base, sinonimos = buscar_definicoes_sinonimos(synsets_target)

        # Definições e traduções no idioma alvo via ILI
        definicoes_target, traducoes_target = buscar_definicoes_traduzidas(synsets_target, w_base,base_lang)



        print("RETORNANDO JSON de DEFINIÇÕES:", {
            "palavra": palavra,
            "base_language": base_lang,
            "target_language": target_lang,
            "definicoes_base": definicoes_base,
            "sinonimos": sinonimos,
            "definicoes_target": definicoes_target,
            "traducoes_target": traducoes_target
        })


        return jsonify({
            "palavra": palavra,
            "base_language": base_lang,
            "target_language": target_lang,
            "definicoes_base": definicoes_base,
            "sinonimos": sinonimos,
            "definicoes_target": definicoes_target,
            "traducoes_target": traducoes_target
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
            if item["key"] == "CHOOSEN_VOICE":
                item["default"] = data["CHOOSEN_VOICE"]
            
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)

        return jsonify({"status": "success"})


    @app.route("/parse_text", methods=["POST"])
    def parse_text():
        # print("FILES:", request.files)
        # print("FORM:", request.form)

        file = request.files.get("file")

        if file is None:
            return "ficheiro não enviado", 400

        return "ok"
    
    @app.route("/search_On_Dict", methods=["POST"])
    def search_On_Dict():
        if not request.is_json:
            return {"error": "Request deve ser JSON"}, 400

        data = request.get_json()

        # pega o objeto interno 'palavra'
        palavra_obj = data.get('palavra', {})
        traducoes = palavra_obj.get('traducoes_target', [])


        print(palavra_obj)

        if not traducoes:
            return {"error": "Nenhuma tradução enviada"}, 400

        alias = app.config['SHORT_TARGET_ALIAS']
        if not alias:
            return {"error": "SHORT_TARGET_ALIAS não configurado"}, 500


        db_options = app.config['DATABASE_DICTIONARY_OPTIONS']
        if alias not in db_options:
            return {"error": f"Alias '{alias}' inválido"}, 500

        db_path = db_options[alias][0]

        resultados = []
        for palavra in traducoes:
            palavra = palavra.strip()
            if not palavra:
                continue
            print("Palavra:", palavra)
            print("Alias:", alias)
            print("DB:", db_path)
            resultado = searchEntry("app/utils/" + db_path, alias, palavra)
            resultados.append({palavra: resultado})
        print(resultados)

        print("RETORNANDO JSON DICIONARIO:", {
            "palavra": palavra,
            "RESULTADO": resultados
        })


        return jsonify({
            "palavra": palavra,
            "resultados":resultados
        })