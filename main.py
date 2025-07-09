import os
import webbrowser
import datetime
import win32com.client
import speech_recognition as sr
from wikipedia import languages

# Initialize Windows SAPI Voice (Text-to-Speech)
speaker = win32com.client.Dispatch("SAPI.SpVoice")





def listen_and_repeat():
    """Listens to user's voice and repeats what they say using Windows SAPI."""
    speaker.Speak("Say something!")
    recognizer = sr.Recognizer()
    recognizer.pause_threshold=1

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
        print("Listening...")
        audio = recognizer.listen(source)  # Capture speech

    try:
        text = recognizer.recognize_google(audio,language='en-in')  # Convert speech to text
        print(f"🗣 You said: {text}")
        speaker.Speak(text)  # Speak the recognized text
        return text  # Return the recognized text
    except sr.UnknownValueError:
        print("❌ Could not understand!")
        speaker.Speak("I couldn't understand you.")
        return None
    except sr.RequestError:
        print("❌ Speech recognition service unavailable!")
        speaker.Speak("Speech recognition service is unavailable.")
        return None


if __name__ == '__main__':
    speaker.Speak("Hello, this is Ember AI")
    sites=[["google","google.com"],["youtube",'youtube.com'],['chess','chess.com']]
    apps=["notepad","calculator"]
    while True:
        text = listen_and_repeat()
        if text and text.lower() == "stop":  # Say "stop" to exit
            speaker.Speak("Goodbye!")
            break
        elif text is None:
            speaker.Speak("No input, sayanora")
            break
        elif "open picture" in text:
            os.startfile(r"picture.png")
        elif "time" in text:
            speaker.Speak("Time is " + datetime.datetime.now().strftime("%I:%M %p"))
        for site in sites:
            if text is not None and f"open {site[0]}" in text.lower():
                speaker.Speak(f"opening {site[0]}")
                webbrowser.open(site[1])
        for app in apps:
            if text is not None and f"open {app}" in text.lower():
                speaker.Speak(f"opening {app}")
                if app=="calculator":
                    os.system("calc")
                else:
                    os.system(f"start {app}")