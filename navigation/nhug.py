import pyttsx3

def speak(text, gender='female', speed=150):
    engine = pyttsx3.init()

    # Setting voice properties
    voices = engine.getProperty('voices')
    if gender.lower() == 'male':
        engine.setProperty('voice', voices[0].id)  # Male voice
    elif gender.lower() == 'female':
        engine.setProperty('voice', voices[1].id)  # Female voice
    else:
        # If gender is not specified, default to female voice
        engine.setProperty('voice', voices[1].id)

    # Setting speech rate
    rate = engine.getProperty('rate')
    engine.setProperty('rate', speed)  # Speed adjustment

    engine.say(text)
    engine.runAndWait()

# Example usage
speak("Hello, how are you today?", gender='female', speed=150)
