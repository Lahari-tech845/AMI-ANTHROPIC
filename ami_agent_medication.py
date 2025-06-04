import speech_recognition as sr
import pyttsx3
import time

recognizer = sr.Recognizer()
tts = pyttsx3.init()

voices = tts.getProperty('voices')
try:
    tts.setProperty('voice', voices[0].id)  # Use David, or switch to [1] for Zira if you prefer
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
        print("Sorry, I didn't catch that. Please try again.")
        speak("Sorry, I didn't catch that. Please try again.")
        return ""

def log_medication_entry(entry):
    with open('medication_log.txt', 'a') as f:
        f.write(entry + '\n')

if __name__ == "__main__":
    speak("Hi John. This is your medication reminder. Have you taken your medicine A?")
    med_response = listen_and_transcribe(timeout=8)
    if med_response:
        log_medication_entry(f"Medication response: {med_response} - Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        if "yes" in med_response:
            speak("Great job staying on track with your medication. Have a wonderful day!")
        elif "no" in med_response:
            speak("Thank you for letting me know. Remember to take your medicine as prescribed, and reach out to your doctor if you have any questions. Have a wonderful day!")
        else:
            speak("Thank you for sharing. Have a wonderful day!")
    else:
        speak("No response was recorded. Please try again later.")
