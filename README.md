Copy and paste the exact markdown text below directly into your `README.md` file.

```markdown
# 🚀 Google IE Student AI Hackathon - Reusable Starter Skeleton

A high-performance, modular full-stack AI boilerplate built with **Python (Flask)**, **vanilla HTML/JS**, and the official **`google-genai` SDK (`gemini-3.6-flash`)**. 

This repository is pre-configured for instant setup so our team can skip backend setup, CORS configuration, and API boilerplate on hackathon day and start building immediately.

---

## ⚡ Quick Start (5-Minute Friday Onboarding)

### 1. Clone the Repository
```bash
git clone <REPOSITORY_URL>
cd WEDNESDAY

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

### 3. Set Up API Keys

Copy `.env.example` to create your local `.env` file:

```bash
# Windows PowerShell
copy .env.example .env

# Mac / Linux
cp .env.example .env

```

Open `.env` and paste your Gemini API key:

```env
GEMINI_API_KEY=AIzaSy...

```

### 4. Run the Backend Server

```bash
python app.py

```

*(Server starts locally at `http://127.0.0.1:5000`)*

### 5. Launch the Frontend

Double-click `index.html` to open the interface directly in your browser.

---

## 📂 Project Structure

```text
WEDNESDAY/
├── .env                 # Private API key storage (DO NOT COMMIT)
├── .env.example         # Template environment file
├── .gitignore           # Git rule file excluding secrets and cache
├── requirements.txt     # Python dependencies
├── app.py               # Flask backend server with Gemini routes
├── index.html           # Modern frontend web interface
├── tools_script.py      # Reference implementation for Function Calling
└── multimodal_script.py # Reference implementation for Image/PDF processing

```

---

## 🛠️ What This Skeleton Can Do

Our boilerplate supports all core Gemini features out-of-the-box:

### 1. Real-Time Text Streaming (`/api/stream`)

* **What it does:** Renders AI responses word-by-word as they generate using `client.models.generate_content_stream()`.
* **Why we use it:** Eliminates perceived loading latency so judges see immediate feedback without staring at loading spinners.

### 2. Guaranteed Structured JSON (`/api/json`)

* **What it does:** Forces Gemini to respond in strict, parseable JSON matching a defined Pydantic schema using `response_schema` and `response_mime_type="application/json"`.
* **Why we use it:** Guarantees zero markdown formatting bugs, allowing us to immediately render incoming data into UI cards, lists, tables, or graphs.

### 3. Autonomous Function Calling / Tool Execution (`tools_script.py`)

* **What it does:** Lets Gemini call local Python functions (like live database lookups, calculation engines, or third-party APIs) automatically when it needs real-time or external data.
* **Why we use it:** Prevents model hallucinations and serves as a major "wow factor" during hackathon demos.

### 4. Multimodal Input Processing (`multimodal_script.py`)

* **What it does:** Directly analyzes images (`PIL.Image`) and multi-page PDF documents (`client.files.upload()`) alongside text prompts.
* **Why we use it:** Allows users to upload screenshots, documents, or photos directly into our app without needing external OCR libraries.

### 5. Built-in Error Fallbacks & Security

* **What it does:** Catches API rate limits, invalid keys, and network timeouts server-side, returning friendly red notification banners to the frontend instead of crashing.

---

## 🎯 How To Morph This for Friday's Theme

On hackathon day, follow these 3 steps to adapt this skeleton to the event prompt:

1. **Change the Target Data Schema (`app.py`):**
Update the Pydantic class in `app.py` to match whatever data structure our project needs:
```python
class ProjectIdea(BaseModel):
    title: str
    summary: str
    tags: list[str]

```


2. **Customize System Prompts (`app.py`):**
Inject persona instructions into the prompt or `config=types.GenerateContentConfig(system_instruction="...")`.
3. **Style the Front-End (`index.html`):**
Modify the HTML layout or attach CSS frameworks (like Tailwind CDN) to make the UI match our product concept.

---

## 🛡️ Important Safety Rules

* **Never commit `.env` to GitHub.** Make sure all secret keys remain in your local `.env` file.
* Always test new routes by handling both success and error responses gracefully.

```

<ElicitationsGroup message="Next steps:">
  <Elicitation label="Perform a clean repository clone test" query="Show me how to run a clean clone test in a separate directory to ensure my teammates won't hit setup issues."/>
  <Elicitation label="Move to Thursday Prep: Hackathon strategy & ideation frameworks" query="Show me the Thursday prep guide covering project selection strategies, hackathon judging criteria, and rapid execution frameworks."/>
</ElicitationsGroup>

```
