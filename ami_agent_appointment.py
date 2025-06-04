import pyttsx3

tts = pyttsx3.init()
voices = tts.getProperty('voices')
try:
    tts.setProperty('voice', voices[0].id)
except IndexError:
    pass

def speak(text):
    tts.say(text)
    tts.runAndWait()

def check_next_appointment():
    try:
        with open('appointments.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    appt_time_str, doctor = line[:16], line[17:]
                    if "2025-06-04" in appt_time_str:
                        speak(f"Hi John. You have an appointment with {doctor} in half an hour. That is today, June 4th at 9 AM.")
                        print(f"Hi John. You have an appointment with {doctor} in half an hour. That is today, June 4th at 9 AM.")
                        return
            speak("No upcoming appointments found, John.")
    except FileNotFoundError:
        speak("No appointments file found.")

if __name__ == "__main__":
    check_next_appointment()
