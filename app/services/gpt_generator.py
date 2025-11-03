import os
from dotenv import load_dotenv
import openai
import json
import re

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
