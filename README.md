# 🚀 AI Career Agent - Smart Job Application & Interview Suite

![Python Version](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Framework-Flask-000000?style=for-the-badge&logo=flask)
![Groq AI](https://img.shields.io/badge/AI-Groq%20Llama%203.3-orange?style=for-the-badge)
![Tavily Search](https://img.shields.io/badge/Search-Tavily%20AI-teal?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

An autonomous, multi-agent AI platform that streamlines the job application process from start to finish. Leveraging **Groq AI (Llama 3.3)** and **Tavily Web Search**, the suite evaluates candidate-job compatibility, scrapes posting URLs, conducts deep company research, tailors resumes, writes cover letters, drafts recruiter outreach messages, and builds custom STAR interview preparation guides.

---

## 🌟 Key Features

### 1. 📊 Candidate-Job Fit Analysis & Match Scorecard
- Calculates a quantitative **Match Score (0–100%)**.
- Highlights **Top Strengths**, **Skill & Experience Gaps**, and **High-Impact Keywords** to emphasize during interviews.

### 2. 🌐 Job Posting URL Auto-Scraper
- Supports both **raw text** job descriptions and direct **HTTP/HTTPS posting URLs**.
- Automatically strips boilerplate navigation/scripts, with fallback web search retrieval if a page is bot-protected.

### 3. 🏢 Real-Time Company & Industry Research
- Uses **Tavily AI Search** to fetch company mission, product offerings, culture, and tech stack insights.

### 4. 📄 Smart Resume Tailoring
- Rewrites resume bullet points to map directly to key job requirements while preserving factual authenticity.

### 5. ✉️ Bespoke Cover Letters
- Drafts personalized cover letter narratives aligned with company values and job expectations.

### 6. 🎯 STAR Method & Technical Interview Prep
- Generates 5 role-specific behavioral questions with **Situation, Task, Action, Result** response strategies.
- Provides technical Q&A and company culture alignment talking points.

### 7. 📩 Recruiter & Hiring Manager Cold Email Generator
- Drafts high-converting **Direct Email** templates and **LinkedIn InMail** messages customized to the candidate and company.

### 8. 📦 DOCX Export & 1-Click ZIP Packaging
- Automatically generates formatted Microsoft Word (`.docx`) files for all assets.
- Provides a single **1-click ZIP package download** containing the complete application bundle.

---

## 🛠️ Multi-Agent Architecture

```text
[Candidate Resume (PDF/DOCX/TXT)] + [Job Description (Text or URL)]
                                │
                                ▼
                       ┌─────────────────┐
                       │  Parser Agent   │ ──► Extract Structured Candidate & Job Metadata
                       └────────┬────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Fit Analyzer  │       │ Researcher    │       │ Resume Tailor │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Cover Letter  │       │ Interview Prep│       │  Cold Email   │
└───────┬───────┘       └───────┬───────┘       └───────┬───────┘
        │                       │                       │
        └───────────────────────┼───────────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Packager Agent  │ ──► Generate DOCX Files & ZIP Archive
                       └─────────────────┘
```

---

## 📂 Project Structure

```text
├── agents/
│   ├── parser.py          # Extracts structured JSON & handles URL scraping
│   ├── researcher.py      # Conducts real-time company web research
│   ├── fit_analyzer.py    # Computes candidate-job match score & gap report
│   ├── resume_tailor.py   # Rewrites experience bullets for JD alignment
│   ├── cover_letter.py    # Drafts personalized cover letters
│   ├── interview_prep.py  # Builds STAR behavioral & technical prep guide
│   ├── cold_email.py      # Generates recruiter outreach email & LinkedIn DMs
│   └── packager.py        # Packages outputs into .docx files & .zip archive
├── tools/
│   ├── pdf_reader.py      # Text extraction from PDF documents
│   ├── docx_writer.py     # Microsoft Word document formatting helpers
│   ├── url_scraper.py     # URL validation, HTML scraping & fallback search
│   └── web_search.py      # Tavily search integration
├── prompts/               # Engineering-optimized LLM prompt templates
├── static/                # Modern CSS (Glassmorphism), JavaScript & UI assets
├── templates/             # HTML5 Jinja templates
├── config.py              # Environment variables & model configuration
├── Procfile               # Production WSGI process configuration
├── requirements.txt       # Project dependencies
├── web.py                 # Flask Web Server entry point
└── main.py                # Command Line Interface (CLI) entry point
```

---

## ⚡ Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/kavyagada20/Job-Application-Agent.git
cd Job-Application-Agent
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

---

## 🖥️ Running the Application

### Option A: Web Application (Flask Dashboard)
```bash
python web.py
```
Open your browser and navigate to `http://localhost:5000`.

### Option B: Command Line Interface (CLI)
```bash
python main.py path/to/resume.pdf "https://example.com/job-posting"
```

---

## ☁️ Deployment Guide

### Deploying to Render (Recommended - Free Tier)

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Deployment setup"
   git push origin main
   ```
2. Log in to **[Render.com](https://render.com)** and click **New +** → **Web Service**.
3. Select your `Job-Application-Agent` GitHub repository.
4. Set the following configuration:
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn web:app`
5. Under **Environment Variables**, add `GROQ_API_KEY` and `TAVILY_API_KEY`.
6. Click **Create Web Service**.

### Deploying to Railway

1. Log in to **[Railway.app](https://railway.app)**.
2. Click **New Project** → **Deploy from GitHub Repo**.
3. Select `Job-Application-Agent`.
4. Add environment variables `GROQ_API_KEY` and `TAVILY_API_KEY`.
5. Railway auto-detects the `Procfile` and deploys your service.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
