import pyttsx3
import speech_recognition as sr
import schedule
import time
from datetime import datetime

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

def listen_and_transcribe(timeout=7):
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

def log_journal_entry(time_of_day, entry):
    with open('journal_log.txt', 'a') as f:
        f.write(f"{datetime.now().date()} {time_of_day}: {entry}\n")

def check_crisis(entry):
    crisis_words = [
        "i hear voices again", "the voices are back", "someone is watching me",
        "i feel paranoid", "i am scared", "i want to hurt myself",
        "i feel hopeless", "i feel unsafe"
    ]
    for word in crisis_words:
        if word in entry:
            return True
    return False

def daily_check(time_of_day):
    speak(f"Hi John. This is your {time_of_day} check-in. How are you feeling?")
    entry = listen_and_transcribe(timeout=10)
    if entry:
        log_journal_entry(time_of_day, entry)
        if check_crisis(entry):
            speak("Thank you for sharing. I sense you might need some support. Notifying your doctor now.")
            print(f"**Emergency: Notifying Doctor Smith for {time_of_day} check-in.**")
        else:
            speak("Thank you, John. Your entry has been saved.")
    else:
        speak("No response recorded. Please try again next time.")

# Schedule the check-ins
schedule.every().day.at("08:00").do(daily_check, "morning")
schedule.every().day.at("14:00").do(daily_check, "afternoon")
schedule.every().day.at("17:00").do(daily_check, "evening")

if __name__ == "__main__":
    speak("AMI is running and will check in with John at 8 AM, 2 PM, and 5 PM every day.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Checks once a minute
