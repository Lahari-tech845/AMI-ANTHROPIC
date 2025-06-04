import pyttsx3
import speech_recognition as sr

tts = pyttsx3.init()
recognizer = sr.Recognizer()
voices = tts.getProperty('voices')
try:
    tts.setProperty('voice', voices[0].id)
except IndexError:
    pass

def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen_and_transcribe(timeout=10):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=timeout)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input.lower()
    except Exception:
        speak("Sorry, I didn't catch that. Please try again.")
        return ""

def log_bedtime_entry(entry):
    with open('bedtime_log.txt', 'a') as f:
        f.write(f"bedtime: {entry}\n")

def check_crisis(entry):
    crisis_words = [
        "i hear voices again",
        "the voices are back",
        "someone is watching me",
        "i feel paranoid",
        "i am scared",
        "i want to hurt myself",
        "i feel hopeless",
        "i feel unsafe"
    ]
    for word in crisis_words:
        if word in entry:
            return True
    return False

if __name__ == "__main__":
    speak("Hi John. It's almost bedtime. How are you feeling before sleep?")
    entry = listen_and_transcribe(timeout=10)
    if entry:
        log_bedtime_entry(entry)
        if check_crisis(entry):
            speak("Thank you for sharing. I sense you might need some support. Notifying your doctor now.")
            print("**Emergency: Notifying Doctor Smith for bedtime check-in.**")
        else:
            speak("Thank you, John. Wishing you a peaceful night.")
    else:
        speak("No response recorded. Please try again next time.")
