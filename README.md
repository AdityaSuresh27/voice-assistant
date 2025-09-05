````markdown
# 🧠 Ember — A Smart Python Voice Assistant

**Ember** is a powerful offline-capable voice assistant built in Python. It listens to your voice, responds intelligently, and can open apps, translate languages, or even run a local AI model for natural conversation — all customizable and privacy-respecting.

> 🛠️ Perfect for hobbyists, tinkerers, and developers looking to explore voice automation and local AI integration.

---

## ✨ Features

- 🎙️ **Voice Command Recognition** — Uses microphone input to capture commands  
- 🌐 **Open Websites & Local Apps** — Launch files, folders, and websites on your system  
- 🌍 **Speech Translation** — Translate spoken sentences into multiple languages  
- 🔊 **Text-to-Speech (TTS)** — Speak out responses using system or custom TTS  
- 🧩 **Modular & Hackable** — Add your own commands, automation, or APIs easily  
- 🧠 **Local AI Chatbot (Ollama + DeepSeek-R1)** — Talk to an offline LLM directly from your app  

---

## 🧪 Requirements

### 📦 Python Dependencies

Install the required libraries:

```bash
pip install SpeechRecognition gTTS playsound pyaudio deep-translator
````

For Windows voice output (optional):

```bash
pip install pywin32
```

---

## 🤖 AI Integration (DeepSeek-R1 via Ollama)

If you'd like to enable **local chatbot functionality**, you can use [Ollama](https://ollama.com/) with the DeepSeek-R1 model:

### 1. 🔧 Install Ollama

Download and install from [https://ollama.com](https://ollama.com).

### 2. 🧠 Download DeepSeek-R1

Run this command once to pull the model:

```bash
ollama run deepseek-r1:1.5b
```
#I used the basic model for my testing, also its free and open source so enjoy

Ollama will handle the download and setup. You don’t need to re-run this every time.

> ✅ Ember connects automatically to the Ollama model when chatbot mode is triggered.

---

## 🚀 How to Run

```bash
python ember.py
```

Speak your command into the microphone(or type it if you want to be boring). The assistant will respond or act accordingly.

---

## 🧠 Example Commands

* `Open Google website`
* `Translate good night to German`
* `Open calculator/notepad`
* `Ember [What you wish to ask]` → enables local chatbot mode with DeepSeek

---

## 📁 Recommended Folder Structure

```
ember-assistant/
├── ember.py
├── picture.png(A random picture which was used initially for testing etc)
└── README.md
```

---

## 🔐 Privacy Notice

This app runs **entirely locally** (except translation, which uses Google Translate API). No voice data is sent to any cloud server.

> For full offline mode, swap in Whisper for STT and MarianMT for translation.


---

