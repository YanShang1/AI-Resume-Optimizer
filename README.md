# AI Resume Optimizer

An AI-powered resume optimization assistant that analyzes a user's resume against a target job description and generates practical improvement suggestions.

## Features

- Upload PDF, DOCX, or TXT resumes
- Paste a target job description
- Analyze resume-job match
- Generate an overall match score
- Identify matched skills
- Identify missing skills
- Rewrite weak resume bullet points
- Generate a targeted professional summary
- Generate an optional cover letter
- Export results as a Markdown report

## Tech Stack

- Python
- Streamlit
- OpenAI API
- PyMuPDF
- python-docx
- python-dotenv

## Project Structure

```text
ai-resume-optimizer/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── src/
│   ├── config.py
│   ├── file_parser.py
│   ├── resume_analyzer.py
│   └── report_generator.py
├── data/
└── assets/
```

## Installation

```bash
git clone https://github.com/your-username/ai-resume-optimizer.git
cd ai-resume-optimizer
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

On Windows, activate the environment with:

```bash
venv\Scripts\activate
```

## Environment Variables

Add your OpenAI API key to `.env`:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

## Resume Description

**AI Resume Optimizer | Python, Streamlit, OpenAI API**

- Built an AI-powered resume optimization tool that analyzes a user's resume against a target job description.
- Implemented PDF/DOCX resume parsing, job requirement extraction, skill gap analysis, and LLM-based resume bullet rewriting.
- Designed structured prompts to generate match scores, missing skills, improved resume bullet points, and personalized professional summaries.
- Developed an interactive Streamlit interface for resume upload, job description input, real-time feedback, and Markdown report export.
