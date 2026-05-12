<<<<<<< HEAD
# 🚀 AI Career Agent

An intelligent, multi-agent orchestration system that automates the tedious parts of job applications. By leveraging **Groq (Llama 3.3-70B)** and **Tavily Search**, this agent researches companies, parses complex documents, and generates high-impact tailored resumes and cover letters in seconds.

## 🌟 Key Features

- **Automated Company Research**: Real-time web scraping to identify company culture, tech stacks, and recent initiatives.
- **Smart Resume Tailoring**: Dynamically re-aligns your experience with specific Job Description (JD) keywords while maintaining factual integrity.
- **Bespoke Cover Letters**: Generates personalized narratives that connect your specific achievements to the company's mission.
- **Multi-Format Parsing**: Robust extraction from PDF, DOCX, and TXT files using advanced text sanitization.
- **Instant Packaging**: Automatically generates and downloads professional `.docx` versions of all tailored materials.

## 🛠️ Tech Stack

- **LLM Orchestration**: [Groq](https://groq.com/) (using `llama-3.3-70b-versatile`)
- **Intelligence**: [Tavily AI](https://tavily.com/) (Real-time Search)
- **Backend**: Python / Flask
- **Frontend**: Tailwind CSS / Vanilla JS (Glassmorphism UI)
- **Document Processing**: `pdfplumber`, `python-docx`

## 📂 Project Structure

```text
├── agents/
│   ├── parser.py          # Extracts structured JSON from Resume/JD
│   ├── researcher.py      # Conducts real-time company web research
│   ├── resume_tailor.py   # Rewrites experience bullets for JD alignment
│   ├── cover_letter.py    # Drafts personalized cover letters
│   └── packager.py        # Orchestrates .docx file generation
├── tools/
│   ├── pdf_reader.py      # Sanitized text extraction from documents
│   ├── docx_writer.py     # Professional document formatting
│   └── web_search.py      # Tavily search implementation
├── prompts/               # Engineering-optimized LLM instructions
├── static/                # Modern UI assets (CSS/JS)
├── templates/             # Flask HTML templates
├── config.py              # Environment and model configuration
└── web.py                 # Flask Application Entry Point
=======
# 🚀 AI Career Agent

An intelligent, multi-agent orchestration system that automates the tedious parts of job applications. By leveraging **Groq (Llama 3.3-70B)** and **Tavily Search**, this agent researches companies, parses complex documents, and generates high-impact tailored resumes and cover letters in seconds.

## 🌟 Key Features

- **Automated Company Research**: Real-time web scraping to identify company culture, tech stacks, and recent initiatives.
- **Smart Resume Tailoring**: Dynamically re-aligns your experience with specific Job Description (JD) keywords while maintaining factual integrity.
- **Bespoke Cover Letters**: Generates personalized narratives that connect your specific achievements to the company's mission.
- **Multi-Format Parsing**: Robust extraction from PDF, DOCX, and TXT files using advanced text sanitization.
- **Instant Packaging**: Automatically generates and downloads professional `.docx` versions of all tailored materials.

## 🛠️ Tech Stack

- **LLM Orchestration**: [Groq](https://groq.com/) (using `llama-3.3-70b-versatile`)
- **Intelligence**: [Tavily AI](https://tavily.com/) (Real-time Search)
- **Backend**: Python / Flask
- **Frontend**: Tailwind CSS / Vanilla JS (Glassmorphism UI)
- **Document Processing**: `pdfplumber`, `python-docx`

## 📂 Project Structure

```text
├── agents/
│   ├── parser.py          # Extracts structured JSON from Resume/JD
│   ├── researcher.py      # Conducts real-time company web research
│   ├── resume_tailor.py   # Rewrites experience bullets for JD alignment
│   ├── cover_letter.py    # Drafts personalized cover letters
│   └── packager.py        # Orchestrates .docx file generation
├── tools/
│   ├── pdf_reader.py      # Sanitized text extraction from documents
│   ├── docx_writer.py     # Professional document formatting
│   └── web_search.py      # Tavily search implementation
├── prompts/               # Engineering-optimized LLM instructions
├── static/                # Modern UI assets (CSS/JS)
├── templates/             # Flask HTML templates
├── config.py              # Environment and model configuration
└── web.py                 # Flask Application Entry Point
>>>>>>> 06116eaa0f9be49c8fcaabd5f2720b3ecc5dc093
