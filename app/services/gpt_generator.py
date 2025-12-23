import os
from dotenv import load_dotenv
import openai
import json
import re
from app.services import extractor
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_test_from_job_description(description_text: str, job_title: str, seniority_input: str,num_questions: int, language_input: str) -> dict:
    prompt = f"""
You are a professional technical test generator with 15+ years of experience designing expert-level assessments for companies like AWS, Oracle, Codility, and McKinsey.

🎯 Your role:
Simulate a real hiring process by generating a **rigorous, domain-specific, and challenging multiple-choice technical test** in **{language_input}**, adapted to the following context:
- **Job Title**: {job_title}
- **Seniority Level**: {seniority_input}
- **Job Description**:
\"\"\"{description_text}\"\"\"

---

🎯 Test Objective:
- Generate **exactly {num_questions} high-quality questions**.
- Reflect difficulty based on seniority:
  - Junior: 70% easy, 30% medium.
  - Mid-Level: 40% medium, 40% hard, 20% expert.
  - Expert: 90% expert-level — include architecture, debugging, scalability, integration, edge cases, design trade-offs, high-stakes real scenarios.

---

⏱ Time Management:
- The full test must be solvable in **15 to 30 minutes maximum**.
- Set `"total_time_limit_minutes"` to an integer between **15 and 30**.
- Each question must include `"estimated_time_seconds"` ≤ 60.

---

💡 Coding Detection & Code Questions:
- Detect if the role involves **software development, scripting, or technical programming**.
- If YES:
  - At least **40% of questions must include code snippets** in the main language (detected from job description).
  - Code should represent **real-world debugging, incomplete logic, faulty design, or algorithmic reasoning**.
  - Code must be readable and properly indented.
  - Code question types:
    - Bug fixing
    - Completion
    - Output prediction
    - Refactoring
    - Trade-off evaluation

---

📚 Question Design Requirements:
- Prioritize **real-world, job-relevant, scenario-based** reasoning.
- Avoid any trivia, textbook definitions, or annotation-only questions.
- Use realistic complexity and require **applied judgment**, **strategic thinking**, and **technical insight**.
- Include:
  - Systems thinking
  - Code evaluation
  - Architectural design choices
  - Data flow, caching, performance bottlenecks
  - Security, integration, CI/CD dilemmas

---

📂 Categories (strict constraint):
- You MUST generate **between 3 and 6 categories maximum — never more**.
- Category names must be **relevant to the job domain**, **short (1–3 words)**, and **non-redundant**.
- Derive them from the job description, but:
  - Merge similar topics (e.g., “Data Modeling” + “Database Design” → “Data Architecture”).
  - Avoid overly narrow names like “Java Loops” or “SEO Keywords”.
  - Use general, conceptual names such as:
    - For IT roles → “Architecture”, “DevOps”, “Code Evaluation”, “Security”, “Integration”, etc.
    - For Data roles → “Data Modeling”, “ETL”, “Visualization”, “Performance”, “Integration”, etc.
    - For Business/HR/Finance → “Analysis”, “Compliance”, “Strategy”, “Operations”, “Optimization”, etc.
- If more than 6 potential categories are detected, **merge or rename them** into broader, meaningful groups.
- Every question must use one of those final 3–6 categories — do NOT invent new ones per question.

---

📋 Per-question format (MUST include):
- `"question"`: realistic, scenario-specific question or code challenge
- `"choices"`: {{"A": "...", "B": "...", "C": "...", "D": "..."}}
- `"correct_answer"`: one letter
- `"explanation"`: concise, precise justification
- `"category"`: thematic domain (e.g., Architecture, DevOps, Code Optimization)
- `"score"`: integer between 5 and 20
- `"estimated_time_seconds"`: realistic solving time ≤ 60

---

📦 Final JSON output:
- `"questions"`: array of all question objects
- `"total_time_limit_minutes"`: total duration (int)
- `"minimum_score_to_pass"`: 70
- `"categories_summary"`: question count per category
- `"estimated_total_time_minutes"`: sum of estimated_time_seconds, in minutes (rounded)
- `"average_time_per_question_seconds"`: average time per question (rounded)

---

⚠️ Rules:
- Do NOT include any markdown, explanations, comments, or headers.
- Do NOT use placeholders like “Code snippet here”.
- Avoid repeat patterns or filler logic.
- Output only a **valid JSON object** — nothing more.

Begin generation now. Output strictly a **valid JSON object**.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are a certified technical test author. You write hard, real-world assessments used in hiring for expert-level roles."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response['choices'][0]['message']['content'].strip()

    cleaned_text = re.sub(r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", result_text, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"=====> failed : {e}\nCleaned response was: {cleaned_text}")



def generate_certification_test_from_course(course_text: str, seniority_input: str, num_questions: int, language_input: str) -> dict:
    prompt = f"""
You are a certified educational assessment designer with 15+ years of experience creating **post-training certification exams** and **hands-on evaluations** for professional learners and developers (e.g., AWS Academy, Coursera, Google Learning).

---

🎯 **Primary Objective**
Your mission is to generate a **professional certification test** that validates whether learners have truly mastered and can apply the knowledge from the provided course.

You must output a **valid JSON object only** (no text, no markdown).

---

📘 **Course Context**
- Learner Level: {seniority_input}
- Language: {language_input}
- Course Content:
\"\"\"{course_text}\"\"\"

---

🧩 **Test Generation Requirements**
1. Generate **exactly {num_questions} unique questions**.  
   - Double-check internally before output: return **exactly** {num_questions}, no more, no less.
2. Each question must:
   - Be **professionally realistic**, **unique**, and **derived** from the course context.
   - Reflect real-world cases (corporate, financial, engineering, auditing, ERP, etc.).
   - Be answerable **without external sources**.
3. Difficulty mix (based on seniority level):
   - Junior: 70% easy, 30% medium  
   - Mid-Level: 40% medium, 40% hard, 20% expert  
   - Expert: 90% expert-level (case-based, analytical, scenario-driven)
4. For expert level, **90% of questions must use applied cases**, and **at least 40% must contain real code snippets** if the course relates to programming, scripting, or software development.

---

💡 **Expert-Level Question Design (MANDATORY for Expert learners)**
Every expert-level question must:
- Begin with a **2–4 line realistic scenario** (corporate or technical).  
- Include a **decision or evaluation** element (choose the optimal policy, design, or solution).  
- Contain at least one **implicit trade-off** (e.g., performance vs cost, compliance vs flexibility, maintainability vs scalability).  
- Use higher-order verbs: *evaluate*, *assess*, *analyze*, *determine*, *justify*, *interpret*, etc.  
- If code is relevant, include syntactically correct and realistic code blocks for:
  - Debugging
  - Refactoring
  - Output prediction
  - Optimization

---

🧠 **Code Inclusion Rules (MANDATORY for Technical Courses)**
If the course mentions **any programming or scripting**:
- ≥ 40% of questions must have **executable or analyzable code snippets**.
- Each snippet must be **syntactically correct** and **contextually meaningful**.
- Use clean indentation and language-specific syntax highlighting.
- No placeholder text like “code snippet here”.
If the course is **not technical**, skip code questions and focus on reasoning or applied case studies.

---

🕒 **Time Constraints**
- `"total_time_limit_minutes"`: between 15 and 30.
- Each `"estimated_time_seconds"` ≤ 60.
- Total time should correspond to the number of questions.

---

📚 **Question Design Guidelines**
- Focus on **applied understanding** and **transfer of knowledge**:
  - Apply a concept to a new context.
  - Identify errors or misconceptions.
  - Evaluate multiple valid approaches.
  - Solve realistic case studies.
- Avoid trivial memorization (like definitions or lists).
- Each question must be **answerable from the course material**, not external sources.

---

📂 **Categories (strict constraint)**
- You MUST create **3 to 6 categories**.
- Categories should be derived from the course topics and be **short, clear, and non-overlapping**.
  Examples:
  - For IT courses: “Syntax”, “Debugging”, “Architecture”, “Performance”, “Security”
  - For Management: “Strategy”, “Leadership”, “Operations”, “Optimization”
- Each question must include a `"category"` field referencing one of these.

---

📋 **Per-question JSON structure**
Each question object must include:
{{
  "question": "...",
  "choices": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "explanation": "Short justification (why this answer is correct)",
  "category": "One of the predefined categories",
  "score": integer between 5 and 20,
  "estimated_time_seconds": integer ≤ 60
}}

---

📦 **Final JSON Output (MUST BE EXACT)**
{{
  "questions": [array of all question objects],
  "total_time_limit_minutes": int (15–30),
  "minimum_score_to_pass": 70,
  "categories_summary": {{"CategoryName": count}},
  "estimated_total_time_minutes": total estimated time (rounded to nearest int),
  "average_time_per_question_seconds": average solving time (rounded)
}}

---

⚠️ **Critical Rules**
- Return **only a valid JSON** — no markdown, no commentary " do not include trailing commas in JSON objects or arrays."

- Verify that `"questions"` array contains exactly {num_questions} elements.
- The correct answers (A, B, C, or D) must be **evenly distributed** across all questions.
- Never repeat the same correct answer more than twice consecutively.
- Randomize the position of the correct answer — avoid systematic placement (e.g., always “B”).
- Do NOT include placeholders like “Code snippet here”.
- Ensure categories_summary matches the count in the questions.
- Be concise but technically accurate.
---

🧰 **Internal Verification (you must do before answering)**
- Count total questions = {num_questions}
- Count categories (3–6)
- Ensure correct answer distribution (A–D balanced)
- Verify at least 40% of code snippets (if technical)


Begin now and return strictly a valid JSON object — nothing else.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are a certified educational test designer specializing in post-training developer certifications."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response['choices'][0]['message']['content'].strip()
    cleaned_text = re.sub(r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", result_text, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"=====> failed : {e}\nCleaned response was: {cleaned_text}")

##########################
# generation depuis le cours dirctement 

def generate_certification_test_from_course22(course_text: str, seniority_input: str, num_questions: int, language_input: str) -> dict:

    prompt = f"""
You are a senior educational assessment architect with 15+ years of experience designing
high-stakes professional certification exams (AWS, Google, SAP, Oracle, ACCA, CPA).

Your task is to generate a VALID, RIGOROUS, NON-TRIVIAL certification exam.

You MUST perform TWO INTERNAL STEPS.
ONLY THE FINAL JSON MUST BE RETURNED.

==================================================
INTERNAL STEP 1 — COURSE INTELLIGENCE EXTRACTION (DO NOT OUTPUT)
==================================================

Deeply analyze the course content and internally identify:

- Core topics (frequently explained, structurally important)
- Secondary topics (supporting concepts)
- Explicit rules, formulas, thresholds, constraints
- Numeric values and calculation mechanisms
- Decision rules and trade-offs
- What learners are expected to DO, not memorize
- Whether the course is technical, financial, legal, or mixed

STRICT RULES:
- Ignore marginal or weakly mentioned topics
- Ignore vague statements without operational meaning
- Never invent missing rules or values

Course Content:
\"\"\"{course_text}\"\"\"

==================================================
INTERNAL STEP 2 — CERTIFICATION EXAM GENERATION
(THIS IS THE ONLY OUTPUT)
==================================================

🎯 PRIMARY OBJECTIVE

Generate a PROFESSIONAL CERTIFICATION EXAM that verifies the learner’s
ABILITY TO APPLY, REASON, CALCULATE, and DECIDE using the course content.

--------------------------------------------------
📘 CONTEXT
- Level: {seniority_input}
- Language: {language_input}

--------------------------------------------------
🧩 GLOBAL CONSTRAINTS

- EXACTLY {num_questions} questions
- NO filler questions
- NO meta-questions
- NO questions about missing information
- Each question must test a REAL competency

--------------------------------------------------
⛔ FORBIDDEN QUESTION TYPES (ABSOLUTE)

- Questions whose correct answer is:
  “Not mentioned”, “None”, “No value specified”
- Pure definition or recall questions
- Procedural sequences without reasoning
- Generic advantages/disadvantages without context

If such a question is generated → DISCARD and regenerate internally.

--------------------------------------------------
🎚 DIFFICULTY MODEL (STRICT)

Junior:
- Requires reasoning, not guessing
- Application of rules, not memorization
- Simple calculations and justified choices
- Application of rules to a concrete situation
- At least one numeric or logical transformation
- Plausible distractors derived from common mistakes

Mid-Level:
- Multi-step reasoning
- Comparison of approaches
- Interpretation of constraints

Expert:
- Scenario-driven (2–4 lines minimum)
- Implicit trade-offs
- Decision justification
- Complex calculations or architecture choices

--------------------------------------------------
⛔ QUESTION QUALITY GATE (MANDATORY)

For EACH question, internally verify:
- The correct answer matches the explanation numerically and logically
- No contradiction in the scenario
- The question requires reasoning or calculation
- The answer cannot be guessed by memorization alone

If any check fails → DISCARD the question and regenerate.

--------------------------------------------------


🧮 CALCULATION RULE (CRITICAL)

If the course includes numeric values, rates, formulas, or thresholds:
- ≥ 30% of questions MUST REQUIRE CALCULATION
- Perform calculations internally step-by-step
- NEVER ask “what is the formula” — ALWAYS APPLY it

==================================================
📊 FINANCIAL, TAX, ECONOMIC & MATH QUESTION ENFORCEMENT
(CRITICAL – DOMAIN-SPECIFIC)
==================================================

If the course domain includes ANY of the following:
- Finance
- Accounting
- Taxation
- Economics
- Payroll
- Financial Mathematics
- Management Control

Then the following rules become MANDATORY:

--------------------------------------------------
1️⃣ QUESTION STRUCTURE (MANDATORY)

Each question MUST:

- Be based on a REALISTIC numeric scenario
  (income, salary, profit, expense, tax base, rate, threshold, period)
- Include AT LEAST two numeric inputs
- Require a transformation of data:
  (calculation, allocation, comparison, marginal impact, net vs gross)

FORBIDDEN:
- “What is the rate…”
- “What is the maximum…”
- “What is the deduction…”
WITHOUT a numeric case.

--------------------------------------------------
2️⃣ CALCULATION DEPTH (STRICT)

For every calculation-based question:
- The learner MUST compute, not recall
- At least ONE intermediate step is required
- Distractors MUST reflect realistic mistakes:
  - wrong tranche
  - forgetting a deduction
  - applying a rate to the wrong base
  - confusing gross vs net

--------------------------------------------------
3️⃣ THEMATIC COVERAGE (MANDATORY BALANCE)

For financial / tax courses, questions MUST span
AT LEAST 3 of the following themes:

- Income / Revenue computation
- Tax base determination
- Progressive or marginal taxation
- Deductions, abatements, exemptions
- Withholding tax vs final tax
- Net vs gross transformation
- Impact of thresholds
- Family or dependency effects
- Period-based reasoning (monthly vs annual)

If thematic diversity < 3 → DISCARD AND REGENERATE.

--------------------------------------------------
4️⃣ ANTI-TRIVIALITY GUARANTEE

A question is INVALID if:
- The answer can be found without calculating
- The explanation is shorter than the question
- Only one number appears in the question
- The learner could answer correctly by guessing

Such questions MUST be discarded internally.

--------------------------------------------------
5️⃣ SENIORITY ADAPTATION (FINANCE-SPECIFIC)

Junior:
- Single rule + numeric application
- One calculation chain
- One correct logic path

Mid-Level:
- Multiple rules combined
- Choice between two calculation approaches
- Impact analysis (before / after deduction)

Expert:
- Multi-period or multi-source income
- Trade-off between tax optimization options
- Justification of the chosen strategy, not only the result

--------------------------------------------------
🧠 TECHNICAL COURSES

If the course is technical:
- ≥ 40% of questions MUST include real, valid code
- Code must be analyzable, executable, or debuggable
- No pseudo-code, no placeholders

If non-technical:
- ZERO code
- Focus on applied reasoning and cases

--------------------------------------------------
📂 CATEGORIES (STRICT)

- Create 3 to 6 CATEGORIES ONLY
- Each category = a competency domain
- Each category MUST have ≥ 2 questions
- Merge topics if needed

--------------------------------------------------
📋 QUESTION FORMAT (MANDATORY)

{{
  "question": "...",
  "choices": {{
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "..."
  }},
  "correct_answer": "A",
  "explanation": "Clear, technical justification",
  "category": "One predefined category",
  "score": 5–20,
  "estimated_time_seconds": ≤ 60
}}

--------------------------------------------------
⚠️ ANTI-DUPLICATION (ABSOLUTE)

- A, B, C, D MUST be different in meaning and value
- Numeric duplicates are forbidden (100 ≠ 100.0 is NOT allowed)
- If duplication detected → regenerate distractor

--------------------------------------------------
📦 FINAL JSON (ONLY THIS)

{{
  "questions": [...],
  "total_time_limit_minutes": 15–30,
  "minimum_score_to_pass": 70,
  "categories_summary": {{"Category": count}},
  "estimated_total_time_minutes": int,
  "average_time_per_question_seconds": int
}}

--------------------------------------------------
🧰 FINAL INTERNAL VERIFICATION (MANDATORY)

Before answering:
- questions.length == {num_questions}
- categories count ∈ [3,6]
- each category ≥ 2 questions
- no forbidden question types
- answer distribution balanced (A–D)
- difficulty matches seniority

If ANY rule fails → regenerate silently.

Return ONLY valid JSON.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.4,
        messages=[
            {
                "role": "system",
                "content": "You are a certified educational test designer specializing in post-training developer certifications."
            },
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response.choices[0].message.content.strip()
    cleaned_text = re.sub(r"```(?:json)?|```", "", result_text).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON parsing failed: {e}\n{cleaned_text}")

##########################
# generation avec modification de extract text labels + contenu réel par thème

def format_course_for_llm(course_data: dict) -> str:
    sections = []

    meta = course_data.get("course_metadata", {})
    sections.append(
        f"""
COURSE METADATA
Title: {meta.get("course_title")}
Domain: {meta.get("domain")}
Language: {meta.get("language")}
"""
    )

    for topic in course_data.get("topics", []):
        sections.append(
            f"""
==============================
TOPIC ID: {topic['topic_id']}
TOPIC LABEL: {topic['topic_label']}
TOPIC TYPE: {topic['topic_type']}

AUTHORITATIVE COURSE SOURCE (THIS TEXT IS THE ONLY TRUTH):
\"\"\"
{topic['source_text']['raw_excerpt']}
\"\"\"

Pedagogical Intent:
- Importance: {topic['pedagogical_role']['importance']}
- Assessment Focus: {topic['pedagogical_role']['assessment_recommendation']}
- Risk of Confusion: {topic['pedagogical_role']['risk_of_confusion']}
"""
        )

    return "\n".join(sections)


def format_objectives_for_llm(course_objectives: dict) -> str:
    lines = ["COURSE LEARNING OBJECTIVES (AUTHORITATIVE):"]

    for obj in course_objectives.get("objectives", []):
        lines.append(
            f"- {obj['objective_id']} ({obj['weight_percentage']}%): {obj['objective_text']}"
        )

    return "\n".join(lines)

def generate_certification_test_from_course11(
    course_structured_data: dict,
    course_objectives: dict,
    seniority_input: str,
    num_questions: int,
    language_input: str
) -> dict:
    """
    Uses the SAME prompt as generate_certification_test_from_course,
    but injects structured course data instead of raw text.
    """

    # 🔁 IMPORTANT: on transforme le JSON structuré en "texte de cours"
    # sans modifier la prompt
    course_text = format_course_for_llm(course_structured_data)
    
    # 2️⃣ extraction + formatage objectifs (SAFE)
    objectives_text = format_objectives_for_llm(course_objectives)


    prompt = f"""
You are a SENIOR UNIVERSITY ASSESSMENT DESIGNER
with 15+ years of experience designing:
- university exams (Licence, Master)
- professional certifications
- post-training evaluations

You strictly respect academic rigor, pedagogical alignment,
and source-based assessment design.

You NEVER introduce external knowledge.

---

🎯 PRIMARY OBJECTIVE

Generate a PROFESSIONAL CERTIFICATION EXAM that verifies
whether learners can UNDERSTAND, APPLY, and REASON
using ONLY the provided course content.

The assessment must be:
- pedagogically sound
- academically defensible
- professionally realistic
- strictly grounded in the provided course content

You MUST return ONLY a VALID JSON OBJECT.
NO explanations. NO markdown. NO comments.

---

============================================================
🎯 LEARNING OBJECTIVES (EXAM BLUEPRINT — MANDATORY)
============================================================

The following learning objectives DEFINE what must be assessed.
They OVERRIDE any importance you might infer from the course.

RULES:
- ALL questions MUST map to ONE objective
- Question distribution MUST respect weight_percentage
- Do NOT generate questions outside these objectives

AUTHORITATIVE OBJECTIVES:
\"\"\"
{objectives_text}
\"\"\"

📘 COURSE CONTEXT

Learner Level: {seniority_input}  
ALL generated content (questions, choices, explanations, categories) MUST be written STRICTLY in: {language_input}


You MUST internally compute:
questions_per_objective = round(weight_percentage × {num_questions} / 100)

If total ≠ {num_questions}, adjust starting from highest-weight objectives.

============================================================
📘 AUTHORITATIVE COURSE CONTENT (ONLY SOURCE OF TRUTH)
============================================================

Learner Level: {seniority_input}
Language: {language_input}

\"\"\"
{course_text}
\"\"\"

---

============================================================
🧩 GLOBAL GENERATION CONSTRAINTS
============================================================

1. Generate **exactly {num_questions} unique questions**
   - No more, no less
   - Internally verify the count before final output

2. Every question MUST:
   - Be derived strictly from the provided course content
   - Be answerable WITHOUT external knowledge
   - Be professionally realistic (academic, corporate, financial, legal, technical, etc.)

3. ABSOLUTE SOURCE RESTRICTION:
   - NEVER introduce concepts, facts, entities, or rules not explicitly present
     in the provided course content.
   - If something is not stated or logically implied in the raw_excerpt,
     it MUST NOT be used.
     
============================================================
ANTI-REDUNDANCY RULE (MANDATORY):
============================================================
- Each DISTINCT rule, condition, or principle from the course
  MAY NOT be used as the primary basis for more than:
  - 2 questions (Junior)
  - 1 question (Mid-Level / Expert)

- If a rule has already been sufficiently assessed,
  you MUST select a different rule or topic.

If no unused rule remains, STOP generating questions.

Two questions are considered REDUNDANT if:
- They lead to the same correct answer
- Using the same rule
- Through the same reasoning path

Changing wording, subject, or examples
does NOT make a question distinct.

Only ONE question per reasoning path is allowed.
============================================================
📚 TOPIC-AWARE PEDAGOGICAL RULES (MANDATORY)
============================================================

Each topic includes:
- topic_type
- raw_excerpt (AUTHORITATIVE SOURCE)

You MUST strictly respect the following mapping:

- If topic_type = "definition" or "concept":
  → Generate understanding, distinction, or interpretation questions ONLY

- If topic_type = "rule" or "classification":
  → Generate application, scope, condition, or reasoning questions ONLY

- If topic_type = "process" or "procedure":
  → Generate sequence, consequence, dependency, or ordering questions ONLY

- If topic_type = "calculation":
  → Generate numerical or logical calculation questions WHEN POSSIBLE

============================================================
🧠 COGNITIVE LEVEL ENFORCEMENT (BLOOM-ALIGNED)
============================================================

For Junior learners:
- ~50% Bloom level 2 (Understanding)
- ~50% Bloom level 3 (Application via simple cases)

For Mid-Level learners:
- ~30% Bloom level 2
- ~50% Bloom level 3
- ~20% Bloom level 4 (Analysis)

For Expert learners:
- ~80–90% Bloom level 4–5 (Analysis & Evaluation)

If the required Bloom level cannot be reached **using ONLY the raw_excerpt**,
DO NOT generate the question.

BLOOM VALIDATION RULE:

Before finalizing each question, internally verify:
- Does the learner need to APPLY, CLASSIFY, or INTERPRET information?
- If the learner can answer by simple recall, the question is INVALID.

INVALID questions MUST be discarded and regenerated.

ANTI-RECALL ENFORCEMENT RULE (MANDATORY):

A question is INVALID if:
- The correct answer can be obtained by directly restating
  a single sentence from the raw_excerpt
- No comparison, classification, or decision is required

Each valid question MUST require at least ONE of:
- distinguishing between two situations
- choosing between two applicable regimes
- excluding at least one plausible but incorrect option

If this condition is not met, regenerate the question.

============================================================
🧪 AUTHORIZED MICRO-CASE CONSTRUCTION
============================================================

You MAY construct simple hypothetical situations (micro-cases)
IF AND ONLY IF ALL conditions below are met:

- Every fact used comes directly from the raw_excerpt
- No new rule, exception, or concept is introduced
- The learner only needs to APPLY, CLASSIFY, or INTERPRET the provided text

These micro-cases MUST remain strictly faithful to the course content.

FOR JUNIOR AND MID-LEVEL LEARNERS:

- At least 60% of questions MUST be formulated as micro-cases
- A micro-case MUST describe a situation involving:
  - a person, a company, or a tax situation
  - followed by a consequence, classification, or applicability question

MICRO-CASE DEPTH REQUIREMENT:

Each micro-case MUST include at least ONE of the following:
- a distinction to be made (resident vs non-resident, IRPP vs IS, etc.)
- a classification decision
- an applicability boundary

If the answer is obvious without comparing options,the question is INVALID.
If this condition is not met, regenerate the question.

============================================================
📌 QUESTION FORM CONSTRAINTS (ANTI-RÉCITATION)
============================================================

DO NOT start questions with:
- "What is..."
- "Which is..."
- "Define..."

MANDATORY QUESTION OPENINGS (for ≥60% of questions):

- "Given the following situation..."
- "In which situation..."
- "What would be the tax consequence if..."
- "How should this situation be treated according to..."
If a question does not involve a situation, consequence, or decision,
it MUST NOT be generated unless explicitly justified by topic_type = definition.


============================================================
🔍 SOURCE TRACEABILITY RULE (NON-NEGOTIABLE)
============================================================

For EVERY generated question:
- The question
- The correct answer
- The explanation

MUST be directly and explicitly traceable
to a sentence, rule, or idea present in the raw_excerpt.

If explicit traceability is not possible:
→ DO NOT generate the question.

============================================================
🎚️ DIFFICULTY DISTRIBUTION (STRICT)
============================================================

- Junior:
  → 40% easy
  → 60% medium

- Mid-Level:
  → 30% medium
  → 50% hard
  → 20% expert

- Expert:
  → 90% expert-level
  → Case-based, analytical, scenario-driven

============================================================
💡 EXPERT-LEVEL DESIGN RULES (IF APPLICABLE)
============================================================

Every expert-level question MUST:
- Start with a **2–4 line realistic scenario**
- Include a **decision, evaluation, or judgment**
- Contain at least ONE implicit trade-off
- Use higher-order verbs:
  evaluate, assess, analyze, determine, justify, interpret

If technical:
- Include realistic, syntactically correct code for:
  debugging, refactoring, output prediction, or optimization

============================================================
🧠 CODE INCLUSION RULES (TECHNICAL COURSES ONLY)
============================================================

If the course mentions programming language or scripting:
- ≥ 40% of questions MUST include code snippets
- Snippets must be executable or analyzable
- No placeholders
- Clean syntax and indentation

If the course is non-technical:
- Do NOT include code
- Focus on reasoning and applied case studies

============================================================
🕒 TIME MANAGEMENT CONSTRAINTS
============================================================

- total_time_limit_minutes: between 15 and 30
- estimated_time_seconds per question ≤ 60
- Total time must be coherent with number of questions

============================================================
📂 CATEGORIES (STRICT CONSTRAINT)
============================================================

============================================================
📂 OBJECTIVE-BASED CATEGORIES (NON-NEGOTIABLE)
============================================================

The exam categories MUST be STRICTLY derived from the learning objectives.

RULES (ABSOLUTE):
- You MUST create EXACTLY one category per learning objective
- You are FORBIDDEN to create any additional categories
- Each question MUST belong to the category corresponding to its mapped_objective_id
- The category label MUST be a concise professional reformulation of the objective text
- Categories MUST remain consistent across all questions


CATEGORY ASSIGNMENT RULE (MANDATORY):

For each question:
- mapped_objective_id = OX
- category MUST be the category associated with OX
- Any mismatch makes the question INVALID

If a question cannot be clearly assigned to ONE objective,
it MUST NOT be generated.

============================================================


============================================================
  SEMANTIC DIVERSITY CHECK (MANDATORY):
============================================================

Before final output:
- Verify that 100% of the output is written in {language_input}
- Compare all questions
- If two questions test the same reasoning with only wording changes,
  KEEP ONLY ONE and regenerate the other.

The final set MUST cover DISTINCT reasoning paths.

============================================================
📋 PER-QUESTION JSON STRUCTURE
============================================================

{{
  "question": "...",
  "choices": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "explanation": "Short justification based strictly on the course text",
  "category": "One predefined category",
  "mapped_objective_id": "O1",
  "score": 5,
  "estimated_time_seconds": 30
}}

============================================================
📦 FINAL JSON OUTPUT (EXACT STRUCTURE)
============================================================

{{
  "questions": [],
  "total_time_limit_minutes": 20,
  "minimum_score_to_pass": 70,
  "categories_summary": {{}},
  "estimated_total_time_minutes": 0,
  "average_time_per_question_seconds": 0
}}

============================================================
⚠️ FINAL CRITICAL RULES
============================================================

- Output ONLY valid JSON
- No trailing commas
- Correct answer distribution must be balanced (A–D)
- Never repeat the same correct answer more than twice consecutively

BEGIN NOW.
Return STRICTLY a valid JSON object — nothing else.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": "You are a certified educational test designer specializing in post-training developer certifications."
            },
            {"role": "user", "content": prompt}
        ]
    )

    raw_text = response.choices[0].message.content.strip()
    cleaned_text = re.sub(r"```(?:json)?|```", "", raw_text).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"[generate_certification_test_from_course11] JSON parse error: {e}\n\n{cleaned_text}"
        )





######################""
def generate_certification_test_from_course11111(course_text: str, seniority_input: str, num_questions: int, language_input: str) -> dict:
    prompt = f"""
You are a certified educational assessment designer with 15+ years of experience creating **post-training certification exams** and **hands-on evaluations** for professional learners and developers (e.g., AWS Academy, Coursera, Google Learning).

---

🎯 **Primary Objective**
Your mission is to generate a **professional certification test** that validates whether learners have truly mastered and can apply the knowledge from the provided course.

You must output a **valid JSON object only** (no text, no markdown).

---

📘 **Course Context**
- Learner Level: {seniority_input}
- Language: {language_input}
- Course Content:
\"\"\"{course_text}\"\"\"

---

🧩 **Test Generation Constraints**
1. You MUST generate **EXACTLY {num_questions} questions** — not one more, not one less.
   - Before answering, count internally to ensure you have exactly {num_questions}.
   - If you generate fewer or more, your answer will be considered invalid.
2. Each question must be unique and domain-relevant.
3. Adapt question difficulty based on {seniority_input}:
   - Junior: 70% easy, 30% medium
   - Mid-Level: 40% medium, 40% hard, 20% expert
   - Expert: 90% expert-level (architecture, debugging, optimization, scalability, integration, design trade-offs)

---

🕒 **Time Constraints**
- `"total_time_limit_minutes"`: between 15 and 30.
- Each `"estimated_time_seconds"` ≤ 60.
- Total time should correspond to the number of questions.

---

💻 **Code Detection & Inclusion (MANDATORY for Technical Courses)**
- If the course includes or references **programming, scripting, or software development**, you MUST include **at least 40% of questions with code snippets**.
- This rule applies even if the course text only indirectly mentions a programming language.
- Code snippets should:
  - Be syntactically correct.
  - Represent **real-world debugging, completion, or optimization** tasks.
  - Have clear, indented formatting.
  - Question types include:
    - Bug fixing
    - Output prediction
    - Refactoring
    - Code completion
    - Performance or logic trade-off

If the course is **not technical**, skip code questions and focus on reasoning or applied case studies.

---

📚 **Question Design Guidelines**
- Focus on **applied understanding** and **transfer of knowledge**:
  - Apply a concept to a new context.
  - Identify errors or misconceptions.
  - Evaluate multiple valid approaches.
  - Solve realistic case studies.
- Avoid trivial memorization (like definitions or lists).
- Each question must be **answerable from the course material**, not external sources.

---

📂 **Categories (strict constraint)**
- You MUST create **3 to 6 categories**.
- Categories should be derived from the course topics and be **short, clear, and non-overlapping**.
  Examples:
  - For IT courses: “Syntax”, “Debugging”, “Architecture”, “Performance”, “Security”
  - For Management: “Strategy”, “Leadership”, “Operations”, “Optimization”
- Each question must include a `"category"` field referencing one of these.

---

📋 **Per-question JSON structure**
Each question object must include:
{{
  "question": "...",
  "choices": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
  "correct_answer": "A",
  "explanation": "Short justification (why this answer is correct)",
  "category": "One of the predefined categories",
  "score": integer between 5 and 20,
  "estimated_time_seconds": integer ≤ 60
}}

---

📦 **Final JSON Output (MUST BE EXACT)**
{{
  "questions": [array of all question objects],
  "total_time_limit_minutes": int (15–30),
  "minimum_score_to_pass": 70,
  "categories_summary": {{"CategoryName": count}},
  "estimated_total_time_minutes": total estimated time (rounded to nearest int),
  "average_time_per_question_seconds": average solving time (rounded)
}}

---

⚠️ **Critical Rules**
- Return **only a valid JSON** — no markdown, no commentary " do not include trailing commas in JSON objects or arrays."

- Verify that `"questions"` array contains exactly {num_questions} elements.
- Do NOT include placeholders like “Code snippet here”.
- Ensure categories_summary matches the count in the questions.
- Be concise but technically accurate.

Begin now and return strictly a valid JSON object — nothing else.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.5,
        messages=[
            {"role": "system", "content": "You are a certified educational test designer specializing in post-training developer certifications."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = response['choices'][0]['message']['content'].strip()
    cleaned_text = re.sub(r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", result_text, flags=re.MULTILINE).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"=====> failed : {e}\nCleaned response was: {cleaned_text}")
