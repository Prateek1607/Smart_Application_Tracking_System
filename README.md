# Smart Application Tracking System (ATS)

> An AI-powered resume analysis and optimization tool that helps job seekers improve their resume's compatibility with Applicant Tracking Systems — built with Streamlit and Google Gemini.

🔗 **[Live App → smartapplicationtrackingsystem.streamlit.app](https://smartapplicationtrackingsystem-trt4zorgjanlfdbhatobz8.streamlit.app)**

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-GPL_v3-blue?style=flat-square)

---

## Project Overview

Smart ATS is a full-stack AI application that simulates how real Applicant Tracking Systems evaluate resumes. The motivation behind this project came from observing how many qualified candidates get filtered out before a human even reads their resume — simply due to poor keyword alignment and formatting.

This tool uses Google's Gemini large language model with carefully engineered prompts to provide structured, rubric-based analysis rather than vague feedback. Every score is computed mathematically using weighted factors derived from published ATS research, making the output reproducible and explainable.

---

## Features

### 1. ATS Score Analysis
- **Overall ATS Score** — computed using real ATS weighting: Keywords (40%), Formatting (25%), Section Structure (12%), Skills Section (12%), Experience (11%)
- **Score Breakdown** — 4 animated score rings for Skills, Experience, Education, and Formatting
- **Role Fit Detection** — compares the candidate's seniority level against the JD requirement (Junior / Mid-Level / Senior / Lead)
- **Missing Keywords** — exact JD keywords not found in the resume
- **Resume Improvement Suggestions** — 3 real weak bullet points from the resume rewritten with strong action verbs, metrics, and relevant tools

### 2. Interview Preparation
- 10 tailored interview questions generated from the specific resume and JD
- Covers technical depth, behavioral (STAR format), situational, and gap-based questions
- Full model answers (8–10 sentences) written in first person using actual resume content

### 3. Cover Letter Generator
- Standard professional business letter format
- Candidate contact details auto-extracted from the resume using regex
- Company name and job title auto-extracted from the JD using the LLM
- Five structured paragraphs including an honest skills gap acknowledgment

### 4. Resume Rewriter
- Complete ATS-optimized rewrite preserving the candidate's original skill category structure
- Missing keywords injected naturally into the appropriate sections
- Weak bullet points replaced with improved versions from the analysis
- Downloadable as a formatted `.docx` file

### 5. Score History Tracker
- Tracks every analysis across the session with timestamps
- Line chart visualizing score improvement over multiple attempts

### 6. PDF Report
- Full downloadable report including scores, keywords, improvements, interview Q&A, and cover letter

---

## Project Structure

```
Smart-ATS/
├── app.py          # Main Streamlit application — UI layout, tabs, session state
├── config.py       # Model initialization and API configuration
├── prompts.py      # All LLM prompts — analysis, interview, rewriter, cover letter
├── helpers.py      # File extraction, response parsers, and UI utility functions
├── pdf_gen.py      # PDF report generation using fpdf2
├── docx_gen.py     # Styled .docx resume output using python-docx
├── styles.py       # Centralized CSS styling
├── requirements.txt
└── .gitignore
```

---

## How the ATS Score is Calculated

The scoring methodology is based on published research on how ATS platforms evaluate resumes. Each factor is scored independently and combined using a weighted average:

| Factor | Weight | Measurement Criteria |
|---|---|---|
| Keyword Match | 40% | Exact JD keywords present in resume (no synonym credit) |
| Formatting | 25% | Standard sections, no tables/graphics, contact info, consistent layout |
| Section Structure | 12% | Presence of Summary, Skills, Experience, Education |
| Skills Section | 12% | Dedicated section, category groupings, JD skill match rate |
| Experience | 11% | Years of experience vs JD requirement and domain alignment |

**Score Formula:**
```
OVERALL = (KEYWORD × 0.40) + (FORMATTING × 0.25) + (STRUCTURE × 0.12) + (SKILLS × 0.12) + (EXPERIENCE × 0.11)
```

The strict keyword matching rule (no synonyms) mirrors how most ATS platforms perform string matching against job postings.

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- A Google API key from [aistudio.google.com](https://aistudio.google.com)

### 1. Clone the repository
```bash
git clone https://github.com/Prateek1607/Smart_Application_Tracking_System.git
cd Smart_Application_Tracking_System
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up your API key
Create a `.env` file in the root folder:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Deployment

This application is deployed on Streamlit Community Cloud and is accessible at the link below.

### Deploy your own instance
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select the forked repo → set main file as `app.py`
4. Under **Advanced settings → Secrets**, add:
```toml
GOOGLE_API_KEY = "your_actual_api_key_here"
```
5. Click **Deploy**

---

## Tech Stack

| Technology | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Web framework and interactive UI |
| [Google Gemini 2.5 Flash](https://ai.google.dev) | LLM for analysis and content generation |
| [PyPDF2](https://pypdf2.readthedocs.io) | PDF resume text extraction |
| [python-docx](https://python-docx.readthedocs.io) | DOCX parsing and formatted output |
| [fpdf2](https://pyfpdf.github.io/fpdf2) | PDF report generation |
| [pandas](https://pandas.pydata.org) | Score history chart data |
| [python-dotenv](https://pypi.org/project/python-dotenv) | Local environment variable management |

---

## Requirements

```
streamlit
PyPDF2
python-docx
google-generativeai
python-dotenv
fpdf2
pandas
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key from aistudio.google.com | ✅ Yes |

---

## Contributing

Contributions, suggestions, and feedback are welcome — especially from fellow students and developers.

1. Fork the repository: [Smart_Application_Tracking_System](https://github.com/Prateek1607/Smart_Application_Tracking_System)
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## License

This project is licensed under the **GNU General Public License v3.0** — see the [LICENSE](LICENSE) file for details.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=flat-square)](https://www.gnu.org/licenses/gpl-3.0)

---

## About the Author

**Prateek Gupta**
AI & Data Science | Python | Machine Learning | NLP

- GitHub: [@Prateek1607](https://github.com/Prateek1607)
- LinkedIn: [@Prateek2518](https://www.linkedin.com/in/prateek2518/)
- Repository: [Smart_Application_Tracking_System](https://github.com/Prateek1607/Smart_Application_Tracking_System)

---

> Built to solve a real problem — helping job seekers get past ATS filters and land more interviews. Feedback and contributions are always appreciated.
