from flask import current_app

def speak_text(text, engine):
    engine.say(text)
    engine.runAndWait()