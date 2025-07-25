import os
import uuid
import webbrowser
import datetime
import threading
import win32com.client
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
from playsound import playsound
import tkinter as tk
from tkinter import scrolledtext

# Initialize voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")

language_map = {
    "english": "en", "hindi": "hi", "malayalam": "ml", "french": "fr",
    "spanish": "es", "german": "de", "tamil": "ta", "telugu": "te",
    "kannada": "kn", "japanese": "ja", "chinese": "zh-CN", "arabic": "ar"
}

apps = ["notepad", "calculator"]

# Text-to-Speech (Google TTS)
def speak_tts(text, lang='en'):
    try:
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        print("TTS error:", e)
        speaker.Speak("Sorry, I could not speak the translated text.")

# Translation handling
def handle_translation(command):
    words = command.lower().split()
    try:
        if "translate" in words and "to" == words[-2]:
            phrase = " ".join(words[1:-2])
            target_lang = words[-1].lower()

            if target_lang not in language_map:
                speaker.Speak(f"Sorry, I don't support translation to {target_lang}")
                return f"Translation not supported for '{target_lang}'"

            translated = GoogleTranslator(source='auto', target=language_map[target_lang]).translate(phrase)
            speaker.Speak(f"In {target_lang}, that is:")
            speak_tts(translated, lang=language_map[target_lang])
            return f"Translated: {translated}"
        else:
            speaker.Speak("Please say: translate something to some language.")
            return "Translation format incorrect."
    except Exception as e:
        speaker.Speak("Sorry, I couldn't translate that.")
        return f"Translation error: {e}"

# Voice input using speech recognition
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speaker.Speak("Say something!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='en-in')
            return text
        except sr.UnknownValueError:
            speaker.Speak("I couldn't understand you.")
            return "Unrecognized speech"
        except sr.RequestError:
            speaker.Speak("Speech recognition service is unavailable.")
            return "Service error"
        except sr.WaitTimeoutError:
            return "No speech detected"

# Command handler
def handle_command(command):
    lower_text = command.lower()
    response = ""

    if "stop" in lower_text:
        speaker.Speak("Goodbye!")
        app.quit()
    elif "open picture" in lower_text:
        os.startfile("picture.png")
        response = "Opened picture.png"
    elif "time" in lower_text:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speaker.Speak(f"Time is {current_time}")
        response = f"Time is {current_time}"
    elif "open" in lower_text and "website" in lower_text:
        l = lower_text.split()
        try:
            web_ind = l.index("open") + 1
            site = l[web_ind]
            webbrowser.open(site + ".com")
            speaker.Speak(f"Opening {site}")
            response = f"Opening website: {site}.com"
        except:
            response = "Could not extract website name."
    elif "translate" in lower_text:
        response = handle_translation(lower_text)
    else:
        for app_name in apps:
            if f"open {app_name}" in lower_text:
                speaker.Speak(f"Opening {app_name}")
                os.system("calc" if app_name == "calculator" else f"start {app_name}")
                response = f"Opening {app_name}"
                break

    return response or "Command processed."

# GUI Setup
app = tk.Tk()
app.title("Ember AI - Chat Assistant")
app.geometry("500x600")

chat_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Segoe UI", 12))
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')

def insert_chat(text, sender="You"):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"{sender}: {text}\n")
    chat_area.see(tk.END)
    chat_area.config(state='disabled')

def process_speech():
    user_input = listen()
    insert_chat(user_input, "You")
    response = handle_command(user_input)
    if response:
        insert_chat(response, "Ember AI")

def on_mic_click():
    threading.Thread(target=process_speech).start()

mic_button = tk.Button(app, text="🎙 Speak", font=("Segoe UI", 14), command=on_mic_click)
mic_button.pack(pady=10)


# Welcome Message
insert_chat("Hello, I am Ember AI. Tap the mic and speak!", "Ember AI")
speaker.Speak("Hello, this is Ember AI")

app.mainloop()
