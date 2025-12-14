#📘 RepoAI – AI-Powered GitHub Repository Analyzer

RepoAI is an AI-powered system that **analyzes GitHub repositories**, **explains what a project does**, **evaluates engineering quality**, and **generates a personalized improvement roadmap**.

It is built for students, developers, recruiters, and hackathon judges who want **fast, objective, and human-readable insights** about any public GitHub repository.

---

## 🚀 Live Demo

* **Frontend (Streamlit):**
  [https://<your-streamlit-app>.streamlit.app](https://repoai-twixihzphrirzki4dbcznp.streamlit.app/)

* **Backend (FastAPI):**
  [https://repoai.onrender.com](https://repoai.onrender.com)

* **Swagger API Docs:**
  [https://repoai.onrender.com/docs](https://repoai.onrender.com/docs)

### 🧪 Try With Example Repository
https://github.com/sanskriti234/RepoAI

---


## 🎯 What Does RepoAI Do?

Given a public GitHub repository URL, RepoAI performs the following:

1. **Repository Understanding**

   * Reads and analyzes `README.md`
   * Explains what the project is about
   * Describes how the system works (high-level workflow)

2. **Repository Quality Evaluation**

   * Project structure analysis
   * Code quality (Pylint score)
   * Cyclomatic complexity (Radon)
   * Documentation quality
   * Testing presence
   * Git practices

3. **Scoring System**

   * Final score out of 100
   * Skill level: Beginner / Intermediate / Advanced
   * Badge: Bronze / Silver / Gold

4. **AI-Powered Improvement Roadmap**

   * Dynamic and repo-specific
   * Prioritized improvement actions
   * Generated using Groq LLM

---

## 🧠 Key Features

* 🔍 Automated GitHub repository analysis
* 📘 README-based project explanation
* 📊 Objective scoring engine
* 🧠 Professional AI-generated summary
* 🛠️ Personalized improvement roadmap
* 🖥️ Interactive Streamlit frontend
* ⚙️ Modular FastAPI backend

---

## 🏗️ System Architecture

```
User
  |
  v
Streamlit Frontend (Cloud)
  |
  |  POST /analyze
  v
FastAPI Backend (Render)
  |
  |-- GitHub Repo Cloning
  |-- Structure Analysis
  |-- Code Quality (radon, pylint)
  |-- README Understanding (LLM)
  |-- Scoring Engine
  |-- AI Roadmap Generation
  v
Groq LLM
```

---

## ⚙️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* GitPython
* Radon
* Pylint
* Groq LLM

### Frontend

* Streamlit
* Requests

### Deployment

* Backend: Render
* Frontend: Streamlit Cloud

---

## 📂 Project Structure

```
RepoAI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   ├── core/
│   │   ├── models/
│   │   └── utils/
│   └── main.py
├── frontend/
│   └── streamlit_app.py
├── requirements.txt
├── render.yaml
└── README.md
```

---

## ▶️ How to Run Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/RepoAI.git
cd RepoAI
```

### 2️⃣ Set Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Backend

```bash
uvicorn backend.app.main:app --reload
```

Backend will be available at:

```
http://127.0.0.1:8000/docs
```

### 5️⃣ Run Frontend

```bash
streamlit run frontend/streamlit_app.py
```

Frontend will be available at:

```
http://localhost:8501
```

---

## 🧪 Example Input

```
https://github.com/MUKUL-TIWARI/ai_avatar_llama
```

---

## 📊 Example Output

* Repository Score: **52 / 100**
* Level: **Intermediate**
* Badge: **Silver**
* Detailed project explanation
* AI-generated improvement roadmap

---

## 🛡️ Notes on Free Deployment

* Render free tier may sleep after inactivity
* First request may take a few seconds
* Retry once if backend is waking up

---

## 🔮 Future Enhancements

* Architecture diagram generation
* README improvement suggestions
* PDF report export
* Repository comparison mode
* Authentication & user dashboards

---

## 👤 Author

Developed by **Sanskriti**

AI + Backend Engineering Project

---

## ⭐ Why RepoAI?

RepoAI goes beyond static analysis by:

* Understanding repositories semantically
* Explaining projects like a human reviewer
* Providing actionable, prioritized guidance

This makes it suitable for **education, hiring, and real-world development workflows**.
