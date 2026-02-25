import io
import re
import PyPDF2 as pdf
import docx


# ── File Extraction ────────────────────────────────────────────────────────────
def extract_pdf(file):
    reader = pdf.PdfReader(file)
    return "".join(p.extract_text() or "" for p in reader.pages)


def extract_docx_text(file):
    d = docx.Document(io.BytesIO(file.read()))
    return "\n".join(p.text for p in d.paragraphs if p.text.strip())


# ── Contact & Job Info Extraction ─────────────────────────────────────────────
def extract_contact_info(resume_text):
    email   = re.search(r'[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}', resume_text)
    phone   = re.search(r'(\+?\d[\d\s\-().]{7,}\d)', resume_text)
    linkedin = re.search(r'linkedin\.com/in/[\w-]+', resume_text, re.IGNORECASE)
    lines = [l.strip() for l in resume_text.splitlines() if l.strip()]
    name = lines[0] if lines else ""
    if name and ("@" in name or "http" in name or len(name.split()) > 5):
        name = ""
    return {
        "name":     name,
        "email":    email.group(0) if email else "",
        "phone":    phone.group(0).strip() if phone else "",
        "linkedin": linkedin.group(0) if linkedin else ""
    }


def extract_job_info(jd_text, model):
    resp = model.generate_content(
        f"Extract ONLY the company name and job title from this job description.\n"
        f"Reply in exactly this format with no other text:\n"
        f"COMPANY: <company name>\nTITLE: <job title>\n\n{jd_text[:2000]}"
    )
    company, title = "", ""
    for line in resp.text.strip().splitlines():
        if line.startswith("COMPANY:"): company = line.split(":", 1)[1].strip()
        if line.startswith("TITLE:"):   title   = line.split(":", 1)[1].strip()
    return company, title


# ── Response Parsers ───────────────────────────────────────────────────────────
def parse_analysis(text):
    out = {
        "skills": 0, "experience": 0, "education": 0, "formatting": 0, "overall": 0,
        "role_level": "", "candidate_level": "", "fit_verdict": "", "fit_reason": "",
        "keywords": [], "improvements": [], "summary": ""
    }
    in_imp = False
    for line in text.strip().splitlines():
        l = line.strip()
        def iv(s): v = s.split(":", 1)[1].strip().replace("%", ""); return int(v) if v.isdigit() else 0
        def sv(s): return s.split(":", 1)[1].strip()
        if   l.startswith("SKILLS_SCORE:"):     out["skills"]          = iv(l)
        elif l.startswith("EXPERIENCE_SCORE:"): out["experience"]      = iv(l)
        elif l.startswith("EDUCATION_SCORE:"):  out["education"]       = iv(l)
        elif l.startswith("FORMATTING_SCORE:"): out["formatting"]      = iv(l)
        elif l.startswith("OVERALL:"):          out["overall"]         = iv(l)
        elif l.startswith("ROLE_LEVEL:"):       out["role_level"]      = sv(l)
        elif l.startswith("CANDIDATE_LEVEL:"):  out["candidate_level"] = sv(l)
        elif l.startswith("FIT_VERDICT:"):      out["fit_verdict"]     = sv(l)
        elif l.startswith("FIT_REASON:"):       out["fit_reason"]      = sv(l)
        elif l.startswith("KEYWORDS:"):
            kw = l.split(":", 1)[1].strip()
            out["keywords"] = [k.strip() for k in kw.split(",") if k.strip() and k.strip().lower() != "none"]
        elif l.startswith("IMPROVEMENTS:"):     in_imp = True
        elif l.startswith("SUMMARY:"):
            in_imp = False
            out["summary"] = sv(l)
        elif in_imp and "BEFORE:" in l and "AFTER:" in l:
            parts = l.lstrip("- ").split("|")
            if len(parts) == 2:
                out["improvements"].append({
                    "before": parts[0].replace("BEFORE:", "").strip(),
                    "after":  parts[1].replace("AFTER:", "").strip()
                })
    return out


def parse_interview(text):
    qa, cur = [], {}
    for l in text.strip().splitlines():
        l = l.strip()
        if re.match(r'^Q\d+:', l):
            if cur: qa.append(cur)
            cur = {"q": re.sub(r'^Q\d+:\s*', '', l), "a": ""}
        elif re.match(r'^A\d+:', l):
            cur["a"] = re.sub(r'^A\d+:\s*', '', l)
    if cur: qa.append(cur)
    return qa


# ── UI Helpers ─────────────────────────────────────────────────────────────────
def score_color(s):
    if s >= 70: return "#16a34a", "rgba(22,163,74,0.15)",  "rgba(22,163,74,0.4)",  "Strong Match 🚀"
    if s >= 45: return "#d97706", "rgba(217,119,6,0.15)",  "rgba(217,119,6,0.4)",  "Moderate Match ⚡"
    return         "#dc2626", "rgba(220,38,38,0.15)",  "rgba(220,38,38,0.4)",  "Low Match 🔧"


def fit_style(verdict):
    if verdict == "Good Fit":      return "#16a34a", "#f0fdf4", "#bbf7d0", "✅"
    if verdict == "Overqualified": return "#d97706", "#fffbeb", "#fde68a", "⚠️"
    return                                "#dc2626", "#fff1f2", "#fecdd3", "❌"


def mini_ring(score, color, label, uid):
    circ = 263.9
    filled = (score / 100) * circ
    return f"""<div class="score-mini">
      <svg viewBox="0 0 100 100" style="width:76px;height:76px;">
        <style>@keyframes r_{uid}{{from{{stroke-dasharray:0 {circ:.1f}}}to{{stroke-dasharray:{filled:.1f} {circ-filled:.1f}}}}}</style>
        <circle cx="50" cy="50" r="42" fill="none" stroke="#f3f4f6" stroke-width="10"/>
        <circle cx="50" cy="50" r="42" fill="none" stroke="{color}" stroke-width="10"
          stroke-linecap="round" transform="rotate(-90 50 50)"
          style="stroke-dasharray:0 {circ:.1f};animation:r_{uid} 1.2s ease forwards 0.3s;"/>
        <text x="50" y="55" text-anchor="middle" fill="{color}"
          font-size="20" font-weight="800" font-family="Inter,sans-serif">{score}%</text>
      </svg>
      <div class="score-mini-label">{label}</div></div>"""
