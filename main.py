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
from tkinter import scrolledtext, Entry
import requests
import json
import subprocess
import time
import requests

def start_ollama_model():
    try:
        # Check if DeepSeek is already running by querying Ollama's API
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "deepseek-r1:1.5b", "prompt": "ping", "stream": False},
            timeout=3
        )
        if res.status_code == 200:
            print("DeepSeek is already running.")
            return
    except:
        print("DeepSeek not running. Starting it...")

    # Start it in a new terminal window so it keeps running
    try:
        subprocess.Popen(
            ["start", "cmd", "/k", "ollama run deepseek-r1:1.5b"],
            shell=True
        )
        time.sleep(5)  # Wait a bit for it to warm up
    except Exception as e:
        print("Error launching DeepSeek:", e)

# Initialize voice
speaker = win32com.client.Dispatch("SAPI.SpVoice")

language_map = {
    "english": "en", "hindi": "hi", "malayalam": "ml", "french": "fr",
    "spanish": "es", "german": "de", "tamil": "ta", "telugu": "te",
    "kannada": "kn", "japanese": "ja", "chinese": "zh-CN", "arabic": "ar"
}

apps = ["notepad", "calculator"]

# ---------- UTILITY FUNCTIONS ----------

def speak_tts(text, lang='en'):
    try:
        filename = f"temp_{uuid.uuid4().hex}.mp3"
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        playsound(filename)
        os.remove(filename)
    except Exception as e:
        speaker.Speak("Sorry, I could not speak that.")

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        speaker.Speak("Say something!")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='en-in')
            return text
        except:
            speaker.Speak("Sorry, I couldn't hear that.")
            return ""

def handle_translation(command):
    words = command.lower().split()
    try:
        if "translate" in words and "to" == words[-2]:
            phrase = " ".join(words[1:-2])
            target_lang = words[-1].lower()

            if target_lang not in language_map:
                speaker.Speak(f"I don't support {target_lang}")
                return f"Translation not supported for '{target_lang}'"

            translated = GoogleTranslator(source='auto', target=language_map[target_lang]).translate(phrase)
            speaker.Speak(f"In {target_lang}, that is:")
            speak_tts(translated, lang=language_map[target_lang])
            return f"Translated: {translated}"
        else:
            speaker.Speak("Use: translate [phrase] to [language].")
            return "Incorrect format."
    except Exception as e:
        speaker.Speak("Translation failed.")
        return f"Translation error: {e}"

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
        now = datetime.datetime.now().strftime("%I:%M %p")
        speaker.Speak(f"The time is {now}")
        response = f"Time is {now}"
    elif "open" in lower_text and "website" in lower_text:
        l = lower_text.split()
        try:
            web_ind = l.index("open") + 1
            site = l[web_ind]
            webbrowser.open(site + ".com")
            speaker.Speak(f"Opening {site}")
            response = f"Opened {site}.com"
        except:
            response = "Could not extract website."
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

def call_ollama(prompt):
    try:
        url = "http://localhost:11434/api/generate"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "deepseek-r1:1.5b",
            "prompt": prompt.replace("Ember", "", 1).strip(),
            "stream": False
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        reply = response.json()['response'].strip()

        # Remove <think> and </think> using plain string ops
        if "<think>" in reply and "</think>" in reply:
            start = reply.find("<think>") + len("<think>")
            end = reply.find("</think>")
            reply = reply[:start - len("<think>")] + reply[start:end] + reply[end + len("</think>"):]

        return reply.strip()
    except Exception as e:
        return f"Ollama error: {e}"


# ---------- GUI ----------

start_ollama_model()
app = tk.Tk()
app.title("Ember AI Chat")
app.geometry("600x700")
app.configure(bg="#1e1e1e")

chat_area = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Segoe UI", 12), bg="#252526", fg="#ffffff", insertbackground='white')
chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_area.config(state='disabled')

def insert_chat(text, sender="You"):
    chat_area.config(state='normal')
    chat_area.insert(tk.END, f"{sender}: {text}\n")
    chat_area.see(tk.END)
    chat_area.config(state='disabled')

# ---------- EVENT HANDLERS ----------

def process_speech():
    user_input = listen()
    if user_input.strip():
        insert_chat(user_input, "You")
        if user_input.lower().startswith("ember"):
            reply = call_ollama(user_input)
        else:
            reply = handle_command(user_input)
        if reply:
            insert_chat(reply, "Ember")
            speaker.Speak(reply)

def on_mic_click():
    threading.Thread(target=process_speech).start()

def on_enter_key(event=None):
    user_input = text_input.get()
    if user_input.strip():
        insert_chat(user_input, "You")
        text_input.delete(0, tk.END)
        threading.Thread(target=process_text, args=(user_input,)).start()

def process_text(user_input):
    if user_input.lower().startswith("ember"):
        reply = call_ollama(user_input)
    else:
        reply = handle_command(user_input)
    if reply:
        insert_chat(reply, "Ember")
        speaker.Speak(reply)

# ---------- UI Controls ----------

input_frame = tk.Frame(app, bg="#1e1e1e")
input_frame.pack(pady=5, fill=tk.X)

text_input = Entry(input_frame, font=("Segoe UI", 13), bg="#2d2d30", fg="white", insertbackground='white')
text_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 5), pady=10)
text_input.bind("<Return>", on_enter_key)

mic_button = tk.Button(input_frame, text="🎙", font=("Segoe UI", 14), command=on_mic_click, bg="#007acc", fg="white", width=4)
mic_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

# ---------- Launch ----------

insert_chat("Hello, I am Ember AI. Type or tap the mic and speak!", "Ember")
speaker.Speak("Hello, this is Ember AI")

app.mainloop()
