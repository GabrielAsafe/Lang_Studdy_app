import pyttsx3

engine = pyttsx3.init()

engine.setProperty('voice', 'roa/pt-br')
engine.setProperty('rate', 130)
engine.setProperty('volume', 0.2)

engine.say("Olá! Agora estou a falar em português.")
engine.runAndWait()
