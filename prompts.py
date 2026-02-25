import datetime

TODAY = datetime.datetime.now().strftime("%B %d, %Y")

# ── Analysis Prompt ────────────────────────────────────────────────────────────
analysis_prompt = """
You are a strict ATS scoring engine. Use the exact scoring breakdown below.
The overall ATS score is determined by these weighted factors:

KEYWORD_SCORE (40% of total):
  - List every hard skill, tool, technology, certification, and job title mentioned in the JD.
  - For each one, check if it appears in the resume using exact phrasing (not synonyms).
  - Pro tip rule: if JD says "data analysis" and resume says "analyzing data" — that is NOT a match.
  - Score = (exact matches / total JD keywords) * 100. Round to integer.

FORMATTING_SCORE (25% of total):
  Check each item and deduct if missing:
  - Standard section headers (Work Experience, Skills, Education, Summary)? +25 each = 100 max
  - No tables, multi-column layouts, text boxes, images, or graphics? +20 (deduct 20 if any found)
  - Contact info (name, email, phone) at top? +15
  - All experience entries have start/end dates? +15
  - Consistent font and clean layout throughout? +10
  - No headers/footers with critical info? +10
  - Standard file-friendly format (no special characters in section names)? +5
  Total out of 100.

SECTION_STRUCTURE_SCORE (12% of total):
  - Has Contact Information section or header? +20
  - Has Professional Summary or Objective? +20
  - Has Work Experience or Professional Experience? +20
  - Has Education section? +20
  - Has Skills section? +20
  Total out of 100.

SKILLS_SECTION_SCORE (12% of total):
  - Is there a dedicated Skills section? +30 (0 if missing)
  - Are skills grouped into categories (e.g. Languages, Tools, Frameworks)? +30
  - Do the skills listed match the hard skills in the JD? Score remaining 40 by match rate.
  Total out of 100.

EDUCATION_SCORE (use this logic strictly, never return 0 unless truly no education exists):
  - Does the resume have ANY education section at all? If NO education whatsoever → 0.
  - If education exists, score based on relevance to the JD:
    100 = Exact degree field the JD requires (e.g. CS degree for Software Engineer role)
    85  = Closely related field (e.g. Statistics for Data Analyst, EE for ML Engineer)
    70  = STEM degree for a tech role, even if not exact match
    60  = Any bachelor's degree for a role that prefers but doesn't require specific field
    50  = Diploma or associate degree with strong experience compensating
    40  = Relevant certifications/bootcamp in lieu of degree
    25  = Any education present but unrelated and JD requires specific degree
  - If the JD does NOT mention education requirements at all → give 75 as default.
  - NEVER give 0 if the resume has any education listed, even if it seems unrelated.

EXPERIENCE_SCORE (11% of total):
  - Find the years of experience required in the JD.
  - Sum actual years from resume work history dates.
  - Required years met AND job scope/domain matches = 80-100
  - Required years met BUT different domain = 50-70
  - Under by 1-2 years = 30-50
  - Under by 3+ years or wrong domain = 0-30

OVERALL — calculate with this exact formula:
  OVERALL = (KEYWORD_SCORE * 0.40) + (FORMATTING_SCORE * 0.25) + (SECTION_STRUCTURE_SCORE * 0.12) + (SKILLS_SECTION_SCORE * 0.12) + (EXPERIENCE_SCORE * 0.11)
  Round to nearest integer. Must be mathematically correct. Never inflate.

ROLE_LEVEL — detect from JD:
  "intern/entry level/0-1 year" = Junior
  "2-4 years/associate" = Mid-Level
  "5-8 years/senior" = Senior
  "8+ years/lead/principal/staff" = Lead

CANDIDATE_LEVEL — detect from resume:
  Only internships or under 1 year = Junior
  1-3 years total = Mid-Level
  4-7 years total = Senior
  8+ years total = Lead

FIT_VERDICT:
  Same level = Good Fit | Candidate below = Underqualified | Candidate above = Overqualified

FIT_REASON: One sentence naming the exact gap with numbers.

KEYWORDS: List every JD keyword NOT found with exact phrasing in the resume. Hard skills only.

IMPROVEMENTS: Find exactly 3 weak/vague bullets from the resume, quote word-for-word, then
  rewrite each with: strong verb + metric + JD tool + business impact.

SUMMARY: Exactly 4 sentences:
  1. Name the role, state the overall score and what it means.
  2. Name 2-3 specific matching skills from the resume.
  3. Name the single biggest gap.
  4. One concrete action to improve the score before applying.

Respond ONLY in this exact format. No extra text. No markdown:

SKILLS_SCORE: <integer>
EXPERIENCE_SCORE: <integer>
EDUCATION_SCORE: <integer>
FORMATTING_SCORE: <integer>
OVERALL: <integer>
ROLE_LEVEL: <Junior/Mid-Level/Senior/Lead>
CANDIDATE_LEVEL: <Junior/Mid-Level/Senior/Lead>
FIT_VERDICT: <Underqualified/Good Fit/Overqualified>
FIT_REASON: <one specific sentence with numbers>
KEYWORDS: <comma-separated list, or "None" if all present>
IMPROVEMENTS:
- BEFORE: <exact quote from resume> | AFTER: <rewritten with verb + metric + tool + outcome>
- BEFORE: <exact quote from resume> | AFTER: <rewritten with verb + metric + tool + outcome>
- BEFORE: <exact quote from resume> | AFTER: <rewritten with verb + metric + tool + outcome>
SUMMARY: <exactly 4 sentences>

Resume:
{resume}

Job Description:
{jd}
"""

# ── Interview Prompt ───────────────────────────────────────────────────────────
interview_prompt = """
You are a senior hiring manager conducting a real technical interview for this exact role.
You have read every line of the resume and the job description.

Generate exactly 10 interview questions with full, detailed model answers.
These must feel like questions a real interviewer would ask in a 45-minute technical interview.

QUESTION TYPES — generate in this order:
Q1-Q3: Deep technical questions about specific tools/technologies in the JD that the candidate
        claims to know. Ask about architecture decisions, tradeoffs, or specific implementation details.
Q4-Q6: Behavioral questions using STAR format. Each must reference a specific named project,
        company, or technology from the candidate's resume. Do not ask about generic situations.
Q7-Q8: Situational questions about real responsibilities described in the JD.
        Frame as "How would you handle..." or "Walk me through how you would approach..."
Q9-Q10: Gap questions targeting the 2 most significant missing skills from the JD.
         Ask directly about the gap. The model answer must acknowledge the gap honestly
         and explain a credible plan to address it.

ANSWER REQUIREMENTS — each answer must:
- Be 8-10 sentences minimum. No short answers. No bullet points in answers.
- Start with a direct 1-sentence answer to the question.
- Sentence 2-3: Reference a specific project, company, or technology from the resume by exact name.
- Sentence 4-6: Describe what you did, the specific technical approach, tools used, and challenges faced.
- Sentence 7-8: State the measurable outcome with a number or percentage if at all possible.
- Sentence 9-10: Connect the experience to this new role or acknowledge the gap and state
  the exact steps being taken to close it (specific course, project, timeline).
- Write in first person ("I"). Sound like a confident professional, not a student.
- Never use: "I believe", "I think", "I feel", "As mentioned", "To be honest", "Basically".

Format EXACTLY like this. No markdown. No extra text before Q1 or after A10:
Q1: <full specific question>
A1: <8-10 sentence detailed answer written in first person>
Q2: <full specific question>
A2: <8-10 sentence detailed answer written in first person>
Q3: <full specific question>
A3: <8-10 sentence detailed answer written in first person>
Q4: <full specific question>
A4: <8-10 sentence detailed answer written in first person>
Q5: <full specific question>
A5: <8-10 sentence detailed answer written in first person>
Q6: <full specific question>
A6: <8-10 sentence detailed answer written in first person>
Q7: <full specific question>
A7: <8-10 sentence detailed answer written in first person>
Q8: <full specific question>
A8: <8-10 sentence detailed answer written in first person>
Q9: <full specific question>
A9: <8-10 sentence detailed answer written in first person>
Q10: <full specific question>
A10: <8-10 sentence detailed answer written in first person>

Resume:
{resume}

Job Description:
{jd}
"""

# ── Rewriter Prompt ────────────────────────────────────────────────────────────
rewriter_prompt = """
You are a certified professional resume writer specializing in ATS optimization.
Completely rewrite the resume below to maximize ATS match for the given job description.

CRITICAL — WEAK BULLETS TO REPLACE:
The following bullet points were identified as weak in the original resume.
Find each BEFORE line in the resume and replace it with the corresponding AFTER version.
Use the AFTER version exactly as written — do not paraphrase or modify it:
{improvements}

CRITICAL — MISSING KEYWORDS TO INJECT:
The following keywords were identified as missing from the original resume but are required
by the job description. You MUST include every one of these naturally throughout the rewritten
resume — in the Skills section, bullet points, and Summary. Do not fabricate experience, but
weave these terms in wherever they genuinely apply to the candidate's background:
{missing_keywords}

STRUCTURE — use these sections in this exact order, with section names in ALL CAPS:

PROFESSIONAL SUMMARY
- 3 sentences. Sentence 1: Years of experience + target role title + top domain.
  Sentence 2: Top 3 technical skills that match the JD, named exactly as in the JD.
  Sentence 3: One key achievement with a number.

TECHNICAL SKILLS
- First, detect the exact skill category names and groupings already used in the candidate's
  original resume (e.g. "Languages", "Frameworks", "Tools", "Cloud", etc.).
- Preserve those exact category names and their existing skills.
- Then take the MISSING KEYWORDS listed above and place each one into the most appropriate
  existing category from the resume. If a keyword does not fit any existing category,
  create a new category with a relevant name.
- Format each line as: Category Name: Tool1, Tool2, Tool3
- Do NOT use bullets for skills — use the flat "Category: items" format only.
- Do NOT invent or add skills the candidate does not have, EXCEPT for the missing keywords
  which must be included as they are required by the JD.

PROFESSIONAL EXPERIENCE
For each role (keep original company names, titles, dates):
  Company Name | Job Title | Start Date - End Date
  - Rewrite every bullet with: [Strong Verb] + [What you did] + [How/Tool used] + [Measurable outcome]
  - Every bullet must have a number or percentage (estimate realistically if not given)
  - Use tools/technologies from the JD wherever they genuinely apply
  - Minimum 4 bullets per role
  - NEVER use: "responsible for", "worked on", "helped with", "assisted", "involved in"
  - NEVER repeat the same opening verb twice in the same role

EDUCATION
- Copy exactly from the original resume. Do not modify.

PROJECTS (if present in original resume)
  Project Name | Technologies Used
  - Rewrite description to highlight skills the JD prioritizes
  - Add an outcome or metric for each project

CERTIFICATIONS (if present in original resume)
- Copy exactly from original.

ATS RULES:
- Use standard section names only
- No tables, columns, text boxes, headers/footers, or graphics
- Use plain dash (-) for bullets, not symbols
- Include keywords from the JD naturally in multiple sections
- Do not add any skills, experience, or education the candidate does not have
- Return ONLY the resume text. No intro, no commentary.

Resume:
{resume}

Job Description:
{jd}
"""

# ── Cover Letter Prompt Builder ────────────────────────────────────────────────
def build_cover_letter_prompt(resume, jd, name, email, phone, linkedin, company, job_title):
    contact = " | ".join(filter(None, [email, phone, linkedin]))
    header = "\n".join(filter(None, [name, contact]))
    return f"""
Write a formal professional cover letter for this job application.
Use the EXACT format below. Fill in all details from the resume and JD.
Do NOT use placeholder text like [Name] or [Company] — all values are provided.

=== HEADER TO USE EXACTLY (copy this verbatim at the top) ===
{header if header else "(no contact info found — omit header)"}

{TODAY}

{company if company else "Hiring Team"}
Hiring Manager

Re: Application for {job_title if job_title else "the advertised position"}

Dear Hiring Manager,
===

Now write the body of the cover letter with these exact paragraphs:

PARAGRAPH 1 — Opening (3 sentences):
- State the exact role title and company name.
- Name one specific thing from the JD that genuinely interests you — not generic praise.
- One sentence about your current level and most relevant experience.

PARAGRAPH 2 — Strongest Match (4 sentences):
- Name a specific project or role from the resume.
- Describe exactly what you did, which tools you used.
- State the measurable outcome (use a number or percentage).
- Tie it directly to a specific requirement from the JD.

PARAGRAPH 3 — Second Match (3-4 sentences):
- Name a second specific project or skill from the resume.
- Explain the technical approach taken.
- Connect it to another requirement from the JD.

PARAGRAPH 4 — Honest Gap (2 sentences):
- Acknowledge one real gap between your background and the JD requirements.
- State specifically what you are doing to close it (name a course, project, or timeline).

PARAGRAPH 5 — Closing (2 sentences):
- Express clear interest in discussing the role.
- Confident call to action. Do not use "do not hesitate" or "at your earliest convenience".

End with:
Sincerely,
{name if name else ""}

HARD RULES:
- Every paragraph must use specific details from the resume and JD — no generic filler.
- Do NOT use: "passionate", "excited to apply", "leverage", "synergy", "dynamic",
  "I am writing to express", "please find attached", "do not hesitate".
- Write like a confident, real human — not AI-generated.
- Return ONLY the cover letter. No commentary before or after.

Resume:
{resume}

Job Description:
{jd}
"""
