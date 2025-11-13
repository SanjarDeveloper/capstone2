# 🎙️ Voice to Image App

> Transform your **voice** into a stunning **AI-generated image** — powered by OpenAI’s Whisper, GPT, and DALL·E 3.

---

## 🧠 Overview

The **Voice to Image App** is a Streamlit-powered web application that converts your short **voice message** into an **AI-generated image**.  
It seamlessly integrates OpenAI’s APIs to transcribe, interpret, and visualize your spoken descriptions.

### ✨ Powered by:
- 🗣️ **Whisper-1** → Speech-to-text transcription  
- 💬 **GPT-3.5-Turbo** → Converts transcript into a creative, vivid image prompt  
- 🎨 **DALL·E 3** → Generates a high-quality image from the refined prompt  

---

## 🔄 Workflow Overview

| Step | Description |
|------|--------------|
| **1️⃣ Input** | Enter your **OpenAI API key** securely in the sidebar. |
| **2️⃣ Upload** | Record and upload an audio file (`.wav`, `.mp3`, `.m4a`, `.ogg`, etc.). |
| **3️⃣ Transcribe** | The app uses **Whisper-1** to transcribe your speech to text. |
| **4️⃣ Prompt Generation** | **GPT-3.5-Turbo** transforms the transcript into a detailed image prompt. |
| **5️⃣ Image Generation** | **DALL·E 3** brings your idea to life as a vivid AI-generated image. |
| **6️⃣ Output** | View your image, the generated prompt, and workflow summary. |

---

## 🖼️ Example Workflow

### 🎧 1. Upload and Configure  
![Step 1: Upload](screenshots/step1.png)  
*Enter API key → Upload your audio file.*

---

### 📝 2. Transcription  
![Step 2: Transcription](screenshots/step2.png)  
*Speech converted to text using Whisper-1.*

---

### 🧩 3. Prompt Generation  
![Step 3: Prompt](screenshots/step3.png)  
*GPT-3.5-Turbo enhances your words into a vivid DALL·E prompt.*

---

### 🌅 4. Image Output  
![Step 4: Output](screenshots/step4.png)  
*DALL·E 3 generates your unique image + full workflow summary.*

---

## ⚙️ Setup Instructions

### 1️. Clone / Create the Project
```bash
git clone https://github.com/SanjarDeveloper/capstone2.git
cd capstone2
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the app:

```bash
streamlit run app.py
```

