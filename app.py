import datetime
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from config import get_model
from prompts import analysis_prompt, interview_prompt, rewriter_prompt, build_cover_letter_prompt
from helpers import (extract_pdf, extract_docx_text, extract_contact_info,
                     extract_job_info, parse_analysis, parse_interview,
                     score_color, fit_style, mini_ring)
from pdf_gen import make_pdf
from docx_gen import make_docx
from styles import CSS

# ── Page Setup ─────────────────────────────────────────────────────────────────
st.set_page_config(page_title="Smart ATS", page_icon="🎯", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

model = get_model()

# ── Session State ──────────────────────────────────────────────────────────────
for k, v in [("result", None), ("qa", []), ("cover", ""), ("rewritten", ""),
             ("history", []), ("resume_text", ""), ("jd_text", ""),
             ("contact", {}), ("job_info", ("", ""))]:
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
# NAVBAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="navbar">
  <div class="navbar-brand">🎯 <span>Smart ATS Analyzer</span></div>
  <div class="navbar-sub">AI-powered resume intelligence</div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# INPUT ROW
# ══════════════════════════════════════════════════════════════════════════════
c1, c2, c3 = st.columns([2, 2, 1], gap="large")

with c1:
    st.markdown('<div class="card"><div class="card-title">📋 Job Description</div>', unsafe_allow_html=True)
    jd = st.text_area("jd", height=240, placeholder="Paste the full job description here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card"><div class="card-title">📄 Your Resume</div>', unsafe_allow_html=True)
    mode = st.radio("mode", ["📎 PDF", "📝 Word (.docx)", "✏️ Type"], horizontal=True, label_visibility="collapsed")
    resume_text = ""
    if mode == "📎 PDF":
        fu = st.file_uploader("pdf", type=["pdf"], label_visibility="collapsed")
        if fu: resume_text = extract_pdf(fu)
    elif mode == "📝 Word (.docx)":
        fu = st.file_uploader("docx", type=["docx"], label_visibility="collapsed")
        if fu: resume_text = extract_docx_text(fu)
    else:
        resume_text = st.text_area("manual", height=180, placeholder="Paste or type your resume here...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="card"><div class="card-title">⚡ Run Analysis</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-size:13px;color:#6b7280!important;-webkit-text-fill-color:#6b7280!important;margin-bottom:8px;">Paste a JD and upload your resume, then click Analyze.</p>', unsafe_allow_html=True)
    analyze = st.button("⚡ Analyze My Resume")
    if st.session_state.result:
        pdf_data = make_pdf(st.session_state.result, st.session_state.qa, st.session_state.cover)
        st.download_button("📥 Full PDF Report", data=pdf_data, file_name="ats_report.pdf", mime="application/pdf")
        if st.session_state.rewritten:
            st.download_button("📄 Rewritten Resume (.docx)",
                data=make_docx(st.session_state.rewritten),
                file_name="rewritten_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    st.markdown('</div>', unsafe_allow_html=True)

# ── Analyze Trigger ────────────────────────────────────────────────────────────
if analyze:
    if not jd.strip():
        st.warning("⚠️ Please paste a job description first.")
    elif not resume_text.strip():
        st.warning("⚠️ Please provide your resume.")
    else:
        with st.spinner("Running full analysis..."):
            resp = model.generate_content(analysis_prompt.format(resume=resume_text, jd=jd))
            st.session_state.result      = parse_analysis(resp.text)
            st.session_state.resume_text = resume_text
            st.session_state.jd_text     = jd
            st.session_state.qa          = []
            st.session_state.cover       = ""
            st.session_state.rewritten   = ""
            st.session_state.contact     = extract_contact_info(resume_text)
            st.session_state.job_info    = extract_job_info(jd, model)
            st.session_state.history.append({
                "date":  datetime.datetime.now().strftime("%b %d, %Y %H:%M"),
                "score": st.session_state.result["overall"],
                "jd_snippet": jd[:60].strip() + "..."
            })
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RESULTS
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.result:
    d = st.session_state.result
    color, bg, border, badge = score_color(d["overall"])
    circ = 263.9
    filled = (d["overall"] / 100) * circ

    if d["overall"] >= 80:
        components.html("""
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
          confetti({particleCount:180,spread:80,origin:{y:0.3},colors:['#6366f1','#a855f7','#ec4899','#f59e0b','#10b981']});
          setTimeout(()=>confetti({particleCount:80,angle:60,spread:55,origin:{x:0}}),400);
          setTimeout(()=>confetti({particleCount:80,angle:120,spread:55,origin:{x:1}}),600);
        </script>""", height=0)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analysis", "🎤 Interview Prep", "✉️ Cover Letter", "📝 Resume Rewriter", "📈 History"
    ])

    # ── TAB 1: Analysis ────────────────────────────────────────────────────
    with tab1:
        st.markdown(f"""
        <div class="score-hero">
          <svg viewBox="0 0 100 100" style="width:120px;height:120px;flex-shrink:0;">
            <style>@keyframes r_ov{{from{{stroke-dasharray:0 {circ:.1f}}}to{{stroke-dasharray:{filled:.1f} {circ-filled:.1f}}}}}</style>
            <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="10"/>
            <circle cx="50" cy="50" r="42" fill="none" stroke="#fff" stroke-width="10"
              stroke-linecap="round" transform="rotate(-90 50 50)"
              style="stroke-dasharray:0 {circ:.1f};animation:r_ov 1.5s ease forwards;"/>
            <text x="50" y="55" text-anchor="middle" fill="#fff"
              font-size="22" font-weight="800" font-family="Inter,sans-serif">{d['overall']}%</text>
          </svg>
          <div>
            <div class="score-hero-label">Overall ATS Match Score</div>
            <div class="score-hero-value">{d['overall']}%</div>
            <span class="score-hero-badge">{badge}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        if d.get("fit_verdict"):
            fc, fbg, fborder, ficon = fit_style(d["fit_verdict"])
            st.markdown(f"""
            <div class="role-fit" style="background:{fbg};border:1.5px solid {fborder};">
              <div class="role-fit-icon">{ficon}</div>
              <div>
                <div class="role-fit-title" style="color:{fc};-webkit-text-fill-color:{fc};">
                  {d['fit_verdict']} — Role expects {d['role_level']}, your resume reads {d['candidate_level']}
                </div>
                <div class="role-fit-reason" style="color:{fc};-webkit-text-fill-color:{fc};">{d['fit_reason']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        bd = [(d["skills"], "#6366f1", "Skills", "sk"), (d["experience"], "#a855f7", "Experience", "ex"),
              (d["education"], "#ec4899", "Education", "ed"), (d["formatting"], "#f59e0b", "Formatting", "fm")]
        st.markdown('<div class="score-grid">' + "".join(mini_ring(s, c, l, u) for s, c, l, u in bd) + '</div>', unsafe_allow_html=True)

        r1, r2 = st.columns([3, 2], gap="large")
        with r1:
            st.markdown('<div class="card"><div class="sec-title" style="color:#6366f1;-webkit-text-fill-color:#6366f1;">📝 Profile Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="summary-body">{d["summary"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with r2:
            st.markdown('<div class="card"><div class="sec-title" style="color:#db2777;-webkit-text-fill-color:#db2777;">🔍 Missing Keywords</div>', unsafe_allow_html=True)
            if d["keywords"]:
                st.markdown('<div class="pill-wrap">' + "".join(f'<span class="pill">{k}</span>' for k in d["keywords"]) + '</div>', unsafe_allow_html=True)
            else:
                st.markdown('<p style="color:#16a34a!important;-webkit-text-fill-color:#16a34a;font-weight:600;">✅ No critical keywords missing!</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if d["improvements"]:
            st.markdown('<div class="card"><div class="sec-title" style="color:#7c3aed;-webkit-text-fill-color:#7c3aed;">✏️ Resume Improvement Suggestions</div>', unsafe_allow_html=True)
            cols = st.columns(len(d["improvements"]), gap="medium")
            for col, imp in zip(cols, d["improvements"]):
                with col:
                    st.markdown(f"""<div class="improve-item">
                      <div class="tag" style="color:#dc2626;-webkit-text-fill-color:#dc2626;">❌ WEAK</div>
                      <div class="box-before">{imp['before']}</div>
                      <div class="box-arrow">↓</div>
                      <div class="tag" style="color:#16a34a;-webkit-text-fill-color:#16a34a;">✅ STRONGER</div>
                      <div class="box-after">{imp['after']}</div></div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: Interview Prep ──────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="card"><div class="sec-title" style="color:#6366f1;-webkit-text-fill-color:#6366f1;">🎤 Interview Question Predictor</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#6b7280!important;-webkit-text-fill-color:#6b7280!important;margin-bottom:4px;">10 role-specific questions with full model answers tailored to your resume.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.qa:
            if st.button("🎤 Generate Interview Questions"):
                with st.spinner("Preparing your interview questions..."):
                    resp = model.generate_content(interview_prompt.format(
                        resume=st.session_state.resume_text, jd=st.session_state.jd_text))
                    st.session_state.qa = parse_interview(resp.text)
                st.rerun()
        else:
            for i, item in enumerate(st.session_state.qa, 1):
                st.markdown(f"""<div class="qa-card">
                  <div class="qa-q">Q{i}. {item['q']}</div>
                  <div class="qa-a">{item['a']}</div></div>""", unsafe_allow_html=True)

    # ── TAB 3: Cover Letter ────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="card"><div class="sec-title" style="color:#db2777;-webkit-text-fill-color:#db2777;">✉️ Cover Letter Generator</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#6b7280!important;-webkit-text-fill-color:#6b7280!important;margin-bottom:4px;">Formal business letter with your real contact info extracted from the resume.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.cover:
            if st.button("✉️ Generate Cover Letter"):
                with st.spinner("Writing your cover letter..."):
                    c = st.session_state.contact
                    company, title = st.session_state.job_info
                    prompt = build_cover_letter_prompt(
                        st.session_state.resume_text, st.session_state.jd_text,
                        c.get("name", ""), c.get("email", ""), c.get("phone", ""),
                        c.get("linkedin", ""), company, title)
                    resp = model.generate_content(prompt)
                    st.session_state.cover = resp.text.strip()
                st.rerun()
        else:
            st.markdown(f'<div class="cover-letter-box">{st.session_state.cover}</div>', unsafe_allow_html=True)
            st.download_button("📥 Download Cover Letter (.docx)",
                data=make_docx(st.session_state.cover),
                file_name="cover_letter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
          
    # ── TAB 4: Resume Rewriter ─────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="card"><div class="sec-title" style="color:#f59e0b;-webkit-text-fill-color:#f59e0b;">📝 ATS Resume Rewriter</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#6b7280!important;-webkit-text-fill-color:#6b7280!important;margin-bottom:4px;">Fully rewritten ATS-optimized resume with improvements + missing keywords injected. Download as .docx.</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if not st.session_state.rewritten:
            if st.button("🔄 Rewrite My Resume"):
                with st.spinner("Rewriting your resume for ATS..."):
                    missing_kw = ", ".join(st.session_state.result.get("keywords", [])) or "None"
                    improvements = st.session_state.result.get("improvements", [])
                    imp_text = "\n".join(
                        f"BEFORE: {i['before']}\nAFTER:  {i['after']}"
                        for i in improvements
                    ) or "None"
                    resp = model.generate_content(rewriter_prompt.format(
                        resume=st.session_state.resume_text,
                        jd=st.session_state.jd_text,
                        missing_keywords=missing_kw,
                        improvements=imp_text
                    ))
                    st.session_state.rewritten = resp.text.strip()
                st.rerun()
        else:
            st.markdown(f'<div class="rewritten-box">{st.session_state.rewritten}</div>', unsafe_allow_html=True)
            st.download_button("📥 Download Updated Resume (.docx)",
                data=make_docx(st.session_state.rewritten),
                file_name="rewritten_resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # ── TAB 5: History ─────────────────────────────────────────────────────
    with tab5:
        st.markdown('<div class="card"><div class="sec-title" style="color:#6366f1;-webkit-text-fill-color:#6366f1;">📈 Resume Score History</div>', unsafe_allow_html=True)
        if len(st.session_state.history) < 2:
            st.markdown('<p style="color:#9ca3af!important;-webkit-text-fill-color:#9ca3af!important;">Run at least 2 analyses to see your progress chart.</p>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame(st.session_state.history)
            st.line_chart(df.set_index("date")["score"], use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.session_state.history:
            st.markdown('<div class="card"><div class="sec-title" style="color:#6b7280;-webkit-text-fill-color:#6b7280;">Past Analyses</div>', unsafe_allow_html=True)
            for h in reversed(st.session_state.history):
                hc, _, _, _ = score_color(h["score"])
                st.markdown(f"""<div class="history-row">
                  <div><div class="history-date">{h['date']}</div>
                  <div class="history-jd">{h['jd_snippet']}</div></div>
                  <div class="history-score" style="color:{hc};-webkit-text-fill-color:{hc};">{h['score']}%</div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            if st.button("🗑️ Clear History"):
                st.session_state.history = []
                st.rerun()
