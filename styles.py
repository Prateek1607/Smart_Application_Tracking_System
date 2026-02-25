CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(160deg, #f0f4ff 0%, #faf5ff 50%, #fff0f9 100%);
    min-height: 100vh;
}
[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent !important; }
.main .block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1400px; }

/* ── Navbar ── */
.navbar { text-align:center; padding:32px 0 28px 0; border-bottom:1.5px solid #e5e7eb; margin-bottom:32px; }
.navbar-brand { font-size:2.6rem; font-weight:800; color:#1e1b4b; -webkit-text-fill-color:#1e1b4b; letter-spacing:-0.5px; line-height:1.2; }
.navbar-brand span { background:linear-gradient(90deg,#6366f1,#a855f7); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }
.navbar-sub { font-size:15px; color:#9ca3af !important; margin-top:6px; -webkit-text-fill-color:#9ca3af !important; }

/* ── Cards ── */
.card { background:#fff; border:1.5px solid #e5e7eb; border-radius:16px; padding:20px 22px; margin-bottom:16px; box-shadow:0 2px 12px rgba(99,102,241,0.05); }
.card-title { font-size:15px; font-weight:700; color:#6366f1; -webkit-text-fill-color:#6366f1; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:12px; }

/* ── Textarea ── */
[data-testid="stTextArea"] textarea { background:#f9fafb !important; border:1.5px solid #e5e7eb !important; border-radius:10px !important; color:#111827 !important; -webkit-text-fill-color:#111827 !important; font-size:13.5px !important; line-height:1.7 !important; padding:11px !important; caret-color:#6366f1 !important; resize:vertical !important; }
[data-testid="stTextArea"] textarea:focus { border-color:#6366f1 !important; box-shadow:0 0 0 3px rgba(99,102,241,0.1) !important; background:#fff !important; }
[data-testid="stTextArea"] textarea::placeholder { color:#9ca3af !important; -webkit-text-fill-color:#9ca3af !important; }
[data-testid="stTextArea"] label { display:none !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] { background:#f9fafb !important; border:1.5px dashed #c7d2fe !important; border-radius:10px !important; padding:4px !important; }
[data-testid="stFileUploader"] label { display:none !important; }
[data-testid="stFileUploader"] * { color:#374151 !important; }
[data-testid="stFileUploader"] small { color:#6b7280 !important; }
[data-testid="stFileUploader"] span { color:#111827 !important; font-weight:500 !important; }
[data-testid="stFileUploader"] button { background:#eef2ff !important; border:1px solid #c7d2fe !important; color:#6366f1 !important; border-radius:8px !important; font-size:13px !important; font-weight:600 !important; }
[data-testid="stFileUploader"] button:hover { background:#e0e7ff !important; border-color:#6366f1 !important; }

/* ── Radio ── */
[data-testid="stRadio"] > div { display:flex !important; flex-direction:row !important; gap:6px !important; }
[data-testid="stRadio"] > div > label { flex:1 !important; text-align:center !important; padding:7px 8px !important; border-radius:8px !important; font-size:12px !important; font-weight:600 !important; border:1.5px solid #e5e7eb !important; background:#f9fafb !important; color:#6b7280 !important; -webkit-text-fill-color:#6b7280 !important; cursor:pointer !important; }
[data-testid="stRadio"] > div > label:has(input:checked) { background:#eef2ff !important; border-color:#6366f1 !important; color:#6366f1 !important; -webkit-text-fill-color:#6366f1 !important; }
[data-testid="stRadio"] > div > label > div:first-child { display:none !important; }
[data-testid="stRadio"] label[data-testid="stWidgetLabel"] { display:none !important; }

/* ── Buttons ── */
div.stButton > button { width:100%; background:linear-gradient(135deg,#6366f1,#a855f7); color:#fff !important; -webkit-text-fill-color:#fff !important; border:none !important; padding:14px 24px !important; border-radius:12px !important; font-size:15px !important; font-weight:700 !important; box-shadow:0 4px 20px rgba(99,102,241,0.3); transition:all 0.2s ease; }
div.stButton > button:hover { box-shadow:0 6px 28px rgba(99,102,241,0.45); transform:translateY(-1px); }
div[data-testid="stDownloadButton"] > button { width:100%; background:#fff !important; color:#6366f1 !important; -webkit-text-fill-color:#6366f1 !important; border:1.5px solid #6366f1 !important; padding:12px 24px !important; border-radius:12px !important; font-size:14px !important; font-weight:700 !important; box-shadow:0 2px 10px rgba(99,102,241,0.1); transition:all 0.2s ease; margin-top:8px !important; }
div[data-testid="stDownloadButton"] > button:hover { background:#eef2ff !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [data-baseweb="tab-list"] { gap:6px; background:transparent; border-bottom:2px solid #e5e7eb; }
[data-testid="stTabs"] [data-baseweb="tab"] { background:#f9fafb; border:1.5px solid #e5e7eb; border-radius:10px 10px 0 0; padding:10px 20px; font-size:13px; font-weight:600; color:#6b7280; -webkit-text-fill-color:#6b7280; }
[data-testid="stTabs"] [aria-selected="true"] { background:#eef2ff !important; border-color:#6366f1 !important; color:#6366f1 !important; -webkit-text-fill-color:#6366f1 !important; }
[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding-top:20px; }

/* ── Score Hero ── */
.score-hero { background:linear-gradient(135deg,#6366f1 0%,#a855f7 100%); border-radius:20px; padding:32px 36px; display:flex; align-items:center; gap:32px; margin-bottom:16px; box-shadow:0 8px 32px rgba(99,102,241,0.35); }
.score-hero-label { font-size:14px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:rgba(255,255,255,0.7); -webkit-text-fill-color:rgba(255,255,255,0.7); margin-bottom:6px; }
.score-hero-value { font-size:4rem; font-weight:800; line-height:1; color:#fff; -webkit-text-fill-color:#fff; margin-bottom:8px; }
.score-hero-badge { display:inline-block; padding:5px 16px; border-radius:20px; font-size:13px; font-weight:700; background:rgba(255,255,255,0.2); color:#fff; -webkit-text-fill-color:#fff; border:1px solid rgba(255,255,255,0.35); }

/* ── Role Fit ── */
.role-fit { border-radius:14px; padding:18px 22px; margin-bottom:16px; display:flex; align-items:flex-start; gap:16px; }
.role-fit-icon { font-size:2rem; flex-shrink:0; }
.role-fit-title { font-size:14px; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; margin-bottom:4px; }
.role-fit-reason { font-size:13px; line-height:1.6; }

/* ── Score Grid ── */
.score-grid { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:16px; }
.score-mini { background:#fff; border:1.5px solid #e5e7eb; border-radius:14px; padding:20px 10px; text-align:center; box-shadow:0 2px 8px rgba(0,0,0,0.04); }
.score-mini-label { font-size:13px; font-weight:700; color:#6b7280; -webkit-text-fill-color:#6b7280; text-transform:uppercase; letter-spacing:0.8px; margin-top:8px; }

/* ── Section Title ── */
.sec-title { font-size:15px; font-weight:700; letter-spacing:1.3px; text-transform:uppercase; margin-bottom:14px; display:flex; align-items:center; gap:7px; }

/* ── Summary & Keywords ── */
.summary-body { font-size:15px; color:#374151; -webkit-text-fill-color:#374151; line-height:1.85; }
.pill-wrap { display:flex; flex-wrap:wrap; gap:8px; }
.pill { padding:5px 13px; border-radius:20px; font-size:13px; font-weight:500; background:#fff1f2; border:1px solid #fecdd3; color:#e11d48; }

/* ── Improvements ── */
.improve-item { margin-bottom:12px; }
.tag { font-size:10px; font-weight:700; letter-spacing:0.8px; margin-bottom:4px; }
.box-before { font-size:13px; line-height:1.6; color:#dc2626; -webkit-text-fill-color:#dc2626; background:#fff1f2; border:1px solid #fecdd3; border-radius:8px; padding:9px 13px; }
.box-arrow { text-align:center; font-size:14px; margin:5px 0; color:#9ca3af; -webkit-text-fill-color:#9ca3af; }
.box-after { font-size:13px; line-height:1.6; color:#16a34a; -webkit-text-fill-color:#16a34a; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:8px; padding:9px 13px; }

/* ── Interview Q&A ── */
.qa-card { background:#f9fafb; border:1.5px solid #e5e7eb; border-radius:12px; padding:18px 20px; margin-bottom:14px; }
.qa-q { font-size:15px; font-weight:700; color:#1e1b4b; -webkit-text-fill-color:#1e1b4b; margin-bottom:10px; line-height:1.5; }
.qa-a { font-size:14px; color:#374151; -webkit-text-fill-color:#374151; line-height:1.85; background:#fff; border-left:3px solid #6366f1; padding:12px 16px; border-radius:0 8px 8px 0; }

/* ── Cover Letter ── */
.cover-letter-box { background:#fff; border:1.5px solid #e5e7eb; border-radius:12px; padding:32px 36px; font-size:14px; color:#1e1b4b; -webkit-text-fill-color:#1e1b4b; line-height:2; white-space:pre-wrap; font-family:'Georgia',serif !important; box-shadow:0 2px 12px rgba(0,0,0,0.05); }

/* ── Resume Rewriter ── */
.rewritten-box { background:#fff; border:1.5px solid #e5e7eb; border-radius:12px; padding:24px 28px; font-size:13.5px; color:#1e1b4b; -webkit-text-fill-color:#1e1b4b; line-height:1.9; white-space:pre-wrap; font-family:'Courier New',monospace !important; box-shadow:0 2px 12px rgba(0,0,0,0.05); }

/* ── History ── */
.history-row { display:flex; align-items:center; justify-content:space-between; padding:12px 16px; background:#f9fafb; border:1.5px solid #e5e7eb; border-radius:10px; margin-bottom:8px; }
.history-date { font-size:12px; color:#9ca3af; -webkit-text-fill-color:#9ca3af; }
.history-jd { font-size:13px; font-weight:600; color:#374151; -webkit-text-fill-color:#374151; }
.history-score { font-size:18px; font-weight:800; }

/* ── Misc ── */
[data-testid="stSpinner"] > div { border-top-color:#6366f1 !important; }
[data-testid="stAlert"] { border-radius:10px !important; }
#MainMenu, footer, [data-testid="stDecoration"] { display:none !important; }
p { color:#6b7280 !important; }
</style>
"""
