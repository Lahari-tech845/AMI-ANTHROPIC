import speech_recognition as sr
import pyttsx3
import time

recognizer = sr.Recognizer()
tts = pyttsx3.init()

voices = tts.getProperty('voices')
for idx, voice in enumerate(voices):
    print(f"{idx}: {voice.name} - {voice.id}")

try:
    tts.setProperty('voice', voices[0].id)
except IndexError:
    pass

def speak(text):
    tts.say(text)
    tts.runAndWait()

def listen_and_transcribe(timeout=5):
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=timeout)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input.lower()
    except Exception as e:
        print("Sorry, I didn't catch that. Please try again.")
        speak("Sorry, I didn't catch that. Please try again.")
        return ""

def log_journal_entry(entry):
    with open('journal_log.txt', 'a') as f:
        f.write(entry + '\n')

def check_crisis(entry):
    crisis_phrases = [
        "i hear voices again",
        "the voices are back",
        "someone is watching me",
        "i feel paranoid",
        "i am scared",
        "i can't trust anyone",
        "i want to hurt myself",
        "i want to disappear",
        "i feel hopeless",
        "people are after me",
        "i want to end it all",
        "i feel unsafe"
    ]
    entry_lower = entry.lower()
    for phrase in crisis_phrases:
        if phrase in entry_lower:
            return True
    return False

def get_confirmation():
    affirmations = ["yes", "yes please", "ok", "okay", "yeah", "sure", "go ahead", "please"]
    for _ in range(2):  # Try twice
        response = listen_and_transcribe(timeout=8)
        if any(word in response for word in affirmations):
            return True
        elif response.strip() == "":
            speak("Sorry, I didn't catch that. Could you please say yes or okay if you want to start?")
    return False

def coping_toolbox():
    speak("Would you like to try a coping activity? You can say breathing, music, or affirmation.")
    user_choice = listen_and_transcribe(timeout=5)
    if "breathing" in user_choice:
        speak("Let's do a breathing exercise. Breathe in through your nose, hold on, and breathe out through your mouth. Shall we start?")
        if get_confirmation():
            time.sleep(1)
            for round in range(2):
                speak("Breathe in")
                time.sleep(1)
                speak("Hold")
                time.sleep(1)
                speak("Breathe out")
                time.sleep(1)
                if round == 0:
                    speak("Repeat")
            speak("Well done. I hope you are feeling better now. Have a wonderful day!")
        else:
            speak("That's okay. If you want to try later, just let me know.")
    elif "music" in user_choice:
        speak("Here's a calming music suggestion. Please visit the link shown on your screen.")
        print("Calming music: https://www.youtube.com/watch?v=2OEL4P1Rz04")
        speak("I hope you are feeling better now. Have a wonderful day!")
    elif "affirmation" in user_choice:
        speak("You are strong, you are valued, and you are not alone. Things can get better, and I am here to support you.")
        speak("I hope you are feeling better now. Have a wonderful day!")
    else:
        speak("That's okay. If you ever want to try a coping activity, just let me know.")

if __name__ == "__main__":
    speak("Hi John. Good morning. How are you feeling today?")
    journal_entry = listen_and_transcribe(timeout=20)
    if journal_entry:
        log_journal_entry(journal_entry)
        if check_crisis(journal_entry):
            speak("Thank you for sharing. I hear that you may be experiencing distressing symptoms. I'm going to notify your doctor or caregiver now, so you can get help. Remember, you are not alone.")
            print("**Crisis detected! Simulating notification to doctor/caregiver.**")
            coping_toolbox()
        else:
            speak("Thank you. I've saved your journal entry for today.")
    else:
        speak("No entry was recorded. Please try again next time.")
