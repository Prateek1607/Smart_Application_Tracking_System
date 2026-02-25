from fpdf import FPDF


def clean(text):
    """Replace unicode characters unsupported by Helvetica with ASCII equivalents."""
    rp = {
        "\u2014": "-", "\u2013": "-", "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"', "\u2022": "*", "\u2026": "...",
        "\u00e9": "e", "\u00e0": "a", "\u00e8": "e", "\u00f1": "n",
        "\u2012": "-", "\u2010": "-", "\u00b7": "*", "\u00a0": " "
    }
    for k, v in rp.items():
        text = text.replace(k, v)
    return text.encode("latin-1", errors="replace").decode("latin-1")


def make_pdf(data, qa=None, cover=None):
    f = FPDF()
    f.add_page()
    L = 20
    f.set_margins(L, 20, 20)
    W = f.w - 2 * L

    def rx(): f.set_x(L)

    def sec(txt):
        f.ln(4); rx()
        f.set_font("Helvetica", "B", 12)
        f.set_text_color(99, 102, 241)
        f.cell(W, 8, txt, ln=True)
        f.set_text_color(55, 65, 81)
        f.ln(1)

    def body(txt, bold=False, size=11):
        rx()
        f.set_font("Helvetica", "B" if bold else "", size)
        f.multi_cell(W, 6, clean(str(txt)))
        rx()

    # Title
    rx(); f.set_font("Helvetica", "B", 20); f.set_text_color(99, 102, 241)
    f.cell(W, 12, "ATS Resume Analysis Report", ln=True, align="C"); f.ln(2)

    # Overall
    rx(); f.set_font("Helvetica", "B", 14); f.set_text_color(30, 27, 75)
    f.cell(W, 9, f"Overall Match: {data['overall']}%", ln=True)
    if data.get("fit_verdict"):
        rx(); f.set_font("Helvetica", "", 11); f.set_text_color(55, 65, 81)
        f.cell(W, 7, f"Role Fit: {data['fit_verdict']} (Role: {data['role_level']} | You: {data['candidate_level']})", ln=True)

    # Score Breakdown
    sec("Score Breakdown")
    for lbl, val in [("Skills", data['skills']), ("Experience", data['experience']),
                     ("Education", data['education']), ("Formatting", data['formatting'])]:
        body(f"  {lbl}: {val}%")

    # Summary
    sec("Profile Summary"); body(data['summary'])

    # Keywords
    sec("Missing Keywords"); body(", ".join(data['keywords']) or "None")

    # Improvements
    sec("Resume Improvement Suggestions")
    for i, imp in enumerate(data['improvements'], 1):
        rx(); f.set_font("Helvetica", "B", 10); f.set_text_color(180, 30, 30)
        f.multi_cell(W, 6, clean(f"[{i}] BEFORE: {imp['before']}")); rx()
        f.set_font("Helvetica", "", 10); f.set_text_color(22, 120, 60)
        f.multi_cell(W, 6, clean(f"    AFTER:  {imp['after']}")); f.ln(2); rx()

    # Interview Q&A
    if qa:
        sec("Interview Questions & Answers")
        for i, item in enumerate(qa, 1):
            rx(); f.set_font("Helvetica", "B", 10); f.set_text_color(30, 27, 75)
            f.multi_cell(W, 6, clean(f"Q{i}: {item['q']}")); rx()
            f.set_font("Helvetica", "", 10); f.set_text_color(55, 65, 81)
            f.multi_cell(W, 6, clean(f"    {item['a']}")); f.ln(2); rx()

    # Cover Letter
    if cover:
        sec("Cover Letter"); body(cover)

    return bytes(f.output())
