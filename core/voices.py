import pyttsx3

def list_voices():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for index, voice in enumerate(voices):
        print(f"Voice {index}: ID: {voice.id}, Name: {voice.name}, Gender: {voice.gender}, Languages: {voice.languages}")

list_voices()
