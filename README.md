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
<img width="1592" height="765" alt="1" src="https://github.com/user-attachments/assets/87342917-a849-4574-a620-4ba4aee007bd" />

>Enter API key → Upload your audio file.

---

### 📝 2. Transcription  
<img width="732" height="203" alt="2" src="https://github.com/user-attachments/assets/5ba390e3-f372-4863-9447-83802a57edc0" /> 


>Speech converted to text using Whisper-1.

---

### 🧩 3. Prompt Generation  
<img width="735" height="416" alt="3" src="https://github.com/user-attachments/assets/477c0ea0-1f5f-4678-bba8-aed85c158806" />

>GPT-3.5-Turbo enhances your words into a vivid DALL·E prompt.

---

### 🌅 4. Image Output  
<img width="719" height="720" alt="4" src="https://github.com/user-attachments/assets/9eef325a-221e-464b-90c7-1309995a6f4a" />  
<img width="732" height="547" alt="5" src="https://github.com/user-attachments/assets/015e2dff-aa34-4ae9-901d-0488fa5cf99d"/>
  

>DALL·E 3 generates your unique image + full workflow summary.

---

## ⚙️ Setup Instructions

### 1️. Clone / Create the Project
```bash
git clone https://github.com/SanjarDeveloper/capstone2.git
cd capstone2
```

### 2. Install dependencies:

```bash
pip install streamlit openai pillow python-dotenv
```

### 3. Start the app:

```bash
streamlit run app.py
```

