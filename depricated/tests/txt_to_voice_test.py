import pyttsx3

engine = pyttsx3.init()


target = 'pt'
voices = engine.getProperty('voices')
chosen_voice = None

for v in voices:
    langs = [lang.decode('utf-8') if isinstance(lang, bytes) else lang for lang in v.languages]

    if any(lang.lower().startswith(target) for lang in langs):
        chosen_voice = v
        print("Voz correspondente encontrada:", v.name)
        break

volume = engine.getProperty('volume')



if chosen_voice:
    engine.setProperty('voice', chosen_voice.id)
else:
    print("Nenhuma voz PT encontrada, usando padrão.")
engine.setProperty('volume', 0.7)
engine.setProperty('rate', 140)

f = open("texto.txt")


rate = engine.getProperty('rate')
engine.say(f.read())
engine.runAndWait()
engine.stop()
