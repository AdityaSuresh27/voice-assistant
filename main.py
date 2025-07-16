import os
import webbrowser
import datetime
import win32com.client
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import os
import uuid

language_map = {
    "english": "en",
    "hindi": "hi",
    "malayalam": "ml",
    "french": "fr",
    "spanish": "es",
    "german": "de",
    "tamil": "ta",
    "telugu": "te",
    "kannada": "kn",
    "japanese": "ja",
    "chinese": "zh-CN",
    "arabic": "ar"
}


def speak_tts(text, lang='en'):
    """Use Google TTS to speak the text aloud in the specified language."""
    try:
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)  # Clean up after playing
    except Exception as e:
        print("TTS error:", e)
        speaker.Speak("Sorry, I could not speak the translated text.")


# Initialize Windows SAPI Voice (Text-to-Speech)
speaker = win32com.client.Dispatch("SAPI.SpVoice")

def handle_translation(command: str):
    words = command.lower().split()
    try:
        if "translate" in words and "to" ==words[len(words)-2]:
            to_index = len(words)-2
            phrase = " ".join(words[1:to_index])  # skip "translate"
            target_lang = words[to_index + 1].lower()

            if target_lang not in language_map:
                speaker.Speak(f"Sorry, I don't support translation to {target_lang}")
                return

            translated = GoogleTranslator(source='auto', target=language_map[target_lang]).translate(phrase)
            print(f"Translated: {translated}")

            speaker.Speak(f"In {target_lang}, that is:")
            speak_tts(translated, lang=language_map[target_lang])

        else:
            speaker.Speak("Please say: translate something to some language.")
    except Exception as e:
        print(f"Translation error: {e}")
        speaker.Speak("Sorry, I couldn't translate that. Please try again.")



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
        print(f"You said: {text}")
        speaker.Speak(text)  # Speak the recognized text
        return text  # Return the recognized text
    except sr.UnknownValueError:
        print(" Could not understand!")
        speaker.Speak("I couldn't understand you.")
        return None
    except sr.RequestError:
        print(" Speech recognition service unavailable!")
        speaker.Speak("Speech recognition service is unavailable.")
        return None


if __name__ == '__main__':
    speaker.Speak("Hello, this is Ember AI")
    
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
        elif "open" in text.lower() and "website" in text.lower():
            l=text.split()
            web_ind=l.index("open")+1
            speaker.Speak(f"opening {l[web_ind]}")
            webbrowser.open(l[web_ind]+".com")
        elif "translate" in text.lower():
            handle_translation(text.lower())
        for app in apps:
            if text is not None and f"open {app}" in text.lower():
                speaker.Speak(f"opening {app}")
                if app=="calculator":
                    os.system("calc")
                else:
                    os.system(f"start {app}")