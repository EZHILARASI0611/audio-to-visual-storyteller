# 🎙️ Generative Audio-to-Visual Educational Storytelling System

An innovative AI/ML pipeline built with Python and Streamlit that transforms spoken audio lectures or short stories into fully structured, visually consistent storyboards in real time.

## 🔗 Project Links & Live Navigation
* **Source Repository:** [View Code on GitHub](https://github.com)
* **Local Web URL:** `http://localhost:8501` (When running on your computer)

---

## 🚀 Key Features
* **Speech-to-Text Processing:** Utilizes OpenAI's Whisper engine to accurately transcribe uploaded audio (`.mp3`, `.wav`, or `.m4a`).
* **Structured Script Orchestration:** Leverages LLM structured inputs (`gpt-4o-mini` paired with Pydantic validation) to break long narrations into individual sequential scenes.
* **Visual Continuity Controls:** Autogenerates complex descriptive context prompts fed directly to image generation layers to guarantee stylistic consistency (e.g., Pixar 3D, Watercolor).

---

## 📐 System Architecture Diagram
[User Audio Upload] ──> [OpenAI Whisper] ──> [Raw Text String]│▼[Streamlit Interface] <── [DALL-E 3 Canvas] <── [LLM Structured JSON Engine]
## 🛠️ Local Installation & Setup

1. **Download the project files or download the source code zip:**
   ```bash
   cd audio-to-visual-storyteller
   ```

2. **Install all required production dependencies:**
   ```bash
   pip install streamlit openai python-dotenv pydantic
   ```

3. **Configure your localized credentials:**
   Create a `.env` file in the root folder and add your private key:
   ```text
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Launch the web service runtime:**
   ```bash
   streamlit run app.py
   ```

---

## 🧰 Tech Stack Employed
* **Frontend UI:** Streamlit Web Framework
* **AI Core Orchestration:** OpenAI API (Whisper-1, GPT-4o-mini, DALL-E 3)
* **Data Typing & Guardrails:** Pydantic Validation
* **Configuration Management:** Python-Dotenv
