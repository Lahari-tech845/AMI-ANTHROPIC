import anthropic
import speech_recognition as sr
import pyttsx3

# Initialize Claude client with your API key
client = anthropic.Anthropic(api_key="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")

# Initialize recognizer and text-to-speech
recognizer = sr.Recognizer()
tts = pyttsx3.init()

def speak(text):
    print(f"AMI (Claude): {text}")
    tts.say(text)
    tts.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=7)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")
        return user_input
    except Exception:
        speak("Sorry, I didn't catch that. Please try again.")
        return ""

def ask_claude(prompt):
    response = client.messages.create(
        model="claude-3-opus-20240229",  # You can also try "claude-3-sonnet-20240229" or "claude-3-haiku-20240307"
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text

if __name__ == "__main__":
    speak("Hi John, I'm AMI. How are you feeling today?")
    while True:
        user_input = listen()
        if not user_input:
            continue
        if user_input.lower() in ["exit", "quit", "bye"]:
            speak("Goodbye, John! Remember, I'm always here for you.")
            break
        ami_reply = ask_claude(user_input)
        speak(ami_reply)
