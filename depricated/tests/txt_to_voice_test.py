import pyttsx3
engine = pyttsx3.init() # object creation

# RATE
rate = engine.getProperty('rate')   # getting details of current speaking rate
print (rate)                        # printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate



target = 'zz'
voices = engine.getProperty('voices')
chosen_voice = None
for v in voices:
    # converte bytes para string se necessário
    langs = [lang.decode('utf-8') if isinstance(lang, bytes) else lang for lang in v.languages]
    print(f"Voz: {v.name}, idiomas: {langs}")

    # verifica se algum idioma da voz começa com o target
    if any(lang.startswith(target) for lang in langs):
        chosen_voice = v
        print("Voz correspondente encontrada:", v.name)
        break


# VOLUME
volume = engine.getProperty('volume')   # getting to know current volume level (min=0 and max=1)
print (volume)                          # printing current volume level
engine.setProperty('volume',1.0)        # setting up volume level  between 0 and 1


voices = engine.getProperty('voices')


# VOICE
# voices = engine.getProperty('voices')       # getting details of current voice
# engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   # changing index, changes voices. 1 for female

engine.say("Hello World!")
engine.say('My current speaking rate is ' + str(rate))
engine.runAndWait()
engine.stop()

# Saving Voice to a file
# On Linux, make sure that 'espeak-ng' is installed
engine.save_to_file('Hello World', 'test.mp3')
engine.runAndWait()




# engine = pyttsx3.init(driverName='espeak')
# engine.setProperty("rate", 125)
# engine.setProperty("volume", 1.0)

# # Lista vozes disponíveis
# voices = engine.getProperty('voices')
# if voices:
#     # Força usar a primeira voz disponível
#     engine.setProperty('voice', voices[0].id)

