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

def listen_and_transcribe(timeout=8):
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

def notify(contact_name, contact_number, message):
    print(f"Simulating notification to {contact_name} ({contact_number}): {message}")

if __name__ == "__main__":
    speak("Hi John. If you are in danger or need immediate help, please say 'SOS'.")
    response = listen_and_transcribe(timeout=8)
    if "sos" in response:
        speak("Emergency detected. Notifying your doctor and family member now.")
        notify("Doctor Smith", "+1-555-123-4567", "Hi Doctor Smith. John has triggered an SOS. Please call him as soon as possible.")
        notify("Jacob", "+1-555-987-6543", "Hi Jacob. John has triggered an SOS emergency. Please check on him right away.")
    else:
        speak("No SOS detected. I am always here if you need help.")
