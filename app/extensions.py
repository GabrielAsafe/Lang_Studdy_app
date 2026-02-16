import pyttsx3
import phunspell
import wn


def init_extensions(app):

    try:
        engine = pyttsx3.init(driverName='espeak')
        engine.setProperty("rate", 125)
        engine.setProperty("volume", 1.0)

        # Lista vozes disponíveis
        voices = engine.getProperty('voices')
        if voices:
            # Força usar a primeira voz disponível
            engine.setProperty('voice', voices[0].id)

        app.tts_engine = engine
    except Exception as e:
        print("⚠️ TTS não inicializado:", e)
        app.tts_engine = None

    #spell checker 
    app.hunspell = phunspell.Phunspell(app.config["TARGET_LANGUAGE"])
    #dictionary
    app.wn_en = wn.Wordnet(lang=app.config["LANGEN"], lexicon=app.config["LEXICONEN"])
    app.wn_pt = wn.Wordnet(lang=app.config["LANG"], lexicon=app.config["LEXICON"])
    app.wn_de = wn.Wordnet(lang=app.config["LANGDE"], lexicon=app.config["LEXICONDE"])
