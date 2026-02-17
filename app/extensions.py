import pyttsx3
import phunspell
import wn
import re
from flask import current_app
import os
import json


def init_extensions(app):
    # agora passamos o app
    define_voices_list(app)

    engine = pyttsx3.init(driverName='espeak')
    engine.setProperty("rate", 125)
    engine.setProperty("volume", 1.0)

    # Escolhe voz
    chosen_voice_name = app.config.get("CHOOSEN_VOICE", "")
    voices = engine.getProperty('voices')
    for v in voices:
        if v.name == chosen_voice_name:
            engine.setProperty('voice', v.id)
            break
    else:
        engine.setProperty('voice', voices[0].id)

    app.tts_engine = engine

    # Spell checker
    app.hunspell = phunspell.Phunspell(app.config["TARGET_LANGUAGE"])

    # WordNet
    app.wn_en = wn.Wordnet(lang=app.config["LANGEN"], lexicon=app.config["LEXICONEN"])
    app.wn_pt = wn.Wordnet(lang=app.config["LANG"], lexicon=app.config["LEXICON"])
    app.wn_de = wn.Wordnet(lang=app.config["LANGDE"], lexicon=app.config["LEXICONDE"])


def init_voice_options():
    engine = pyttsx3.init(driverName='espeak')
    voices = engine.getProperty('voices')

    voice_options = {}  # dicionário {nome da voz: idiomas}

    for v in voices:
        langs = [lang.decode('utf-8') if isinstance(lang, bytes) else lang for lang in v.languages]
        voice_options[v.name] = langs

    return voice_options


def define_voices_list(app):
    config_path = os.path.join(app.root_path, "static", "conf.json")
    
    default = ''

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    for item in config["configurations"]:
        if item["key"] == "CHOOSEN_VOICE":
            default = item['default']
        if item["key"] == "VOICE_OPTIONS":
            item["options"] = init_voice_options()
        if item["key"] == "SHORT_TARGET_ALIAS":
            item["default"] = default[:2]  # pega os 2 primeiros caracteres da voz escolhida


    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


