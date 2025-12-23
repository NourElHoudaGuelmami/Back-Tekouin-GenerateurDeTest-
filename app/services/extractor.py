import os
from dotenv import load_dotenv
import openai
import json
import re


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_course_objectives(objectives_text: str) -> dict:
    if not objectives_text or len(objectives_text.strip()) < 50:
        raise ValueError("Objectives PDF text is empty or too short")

    prompt = f"""
You are a senior academic curriculum engineer.

Your task is to extract ONLY the LEARNING OBJECTIVES from the document below.

STRICT RULES:
- Extract ONLY objectives (ignore intro, examples, explanations)
- Use the EXACT wording from the document
- Do NOT invent objectives
- Do NOT summarize
- If objectives are implicit, extract the closest explicit sentences

OUTPUT FORMAT (VALID JSON ONLY):

{{
  "objectives": [
    {{
      "objective_id": "O1",
      "objective_text": "",
      "weight_percentage": 0
    }}
  ]
}}

WEIGHT RULES:
- Total weight_percentage MUST equal 100
- Core objectives = higher weight
- Minor objectives = lower weight

DOCUMENT:
\"\"\"
{objectives_text}
\"\"\"

Return ONLY valid JSON. No markdown. No commentary.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": "You extract academic objectives with zero hallucination."
            },
            {"role": "user", "content": prompt}
        ]
    )

    raw = response.choices[0].message.content.strip()

    # 🔥 DEBUG CRITIQUE (OBLIGATOIRE)
    print("\n===== RAW GPT OBJECTIVES OUTPUT =====")
    print(raw)
    print("====================================\n")

    cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()

    if not cleaned.startswith("{"):
        raise ValueError(
            "GPT did not return JSON for objectives extraction:\n" + cleaned[:500]
        )

    return json.loads(cleaned)




def extract_course_data11(course_text: str) -> dict:
    prompt = f"""
You are a senior instructional designer and academic content analyst.

Your task is to extract and STRUCTURE the course content below WITHOUT interpretation.
This structured output will be used as the ONLY knowledge source for exam generation.

⚠️ CRITICAL RULES (NON-NEGOTIABLE):
- Do NOT summarize, rephrase, or infer.
- Use ONLY the exact wording from the course when capturing content.
- Every topic MUST include the original source text excerpt.
- If something is unclear or fragmented, capture it as-is.
- NEVER add external knowledge.

---

🎯 OUTPUT FORMAT (VALID JSON ONLY)

{{
  "course_metadata": {{
    "course_title": "",
    "domain": "",
    "language": "",
    "source_type": "pdf",
    "extraction_confidence": "high | medium | low"
  }},
  "topics": [
    {{
      "topic_id": "T1",
      "topic_label": "",
      "topic_type": "definition | rule | process | calculation | classification | exception | concept | procedure | case",
      "source_text": {{
        "raw_excerpt": "",
        "start_context": "",
        "end_context": ""
      }},
      "structured_content": {{
        "definitions": [],
        "key_points": [],
        "rules": [],
        "constraints": [],
        "exceptions": [],
        "steps": [],
        "values": [
          {{
            "label": "",
            "value": "",
            "unit": "",
            "context": ""
          }}
        ],
        "examples": []
      }},
      "pedagogical_role": {{
        "importance": "core | important | complementary",
        "assessment_recommendation": "memorization | application | calculation | case_analysis",
        "risk_of_confusion": "low | medium | high"
      }}
    }}
  ]
}}

---

📘 COURSE CONTENT
\"\"\"{course_text}\"\"\"

Return ONLY valid JSON. No markdown. No commentary.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.1,
        messages=[
            {"role": "system", "content": "You extract academic content with zero hallucination."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)








def extract_job_data(job_description_text: str) -> dict:
    
    categories = ["Industries agro-alimentaires","AIndustrie Automobile","Industrie Electronique","Industrie Pharmaceutique","Industries des matériaux de construction",
                  "Industries mécaniques et métallurgiques","Industries électriques, électroniques et de l'électroménager","Industries chimiques","Industries textiles et habillement",
                  "Industries du bois, du liège et de l'ameublement","Industries Emballages","Industries diverses","Grande Distribution","Juridique",
                  "Assurance, Banques, Finances","Informatique et Nouvelles Technologies","Télécommunication","Enseignement","Santé","Commerce",
                  "E-Commerce","Hôtellerie, Tourisme, Loisirs","Environnement","BTP","Autres Services"]
    prompt = f'''
As a hiring manager, your task is to extract every mandatory and optional technical skill,
along with the required years of experience, from the provided job description.
Translate the text to English and return the extracted information in the following JSON format as fast as you possibly can.
Classify it into one of these categories: {', '.join(categories)}.
       
{{
"mandatory_technical_skills": [List of mandatory technical skills],
"optional_skills": [],
"function_title":"",
"required_years_of_experience": integer number of years of experience 0 if it's not mentioned,
"required_industry_verticals":"example banking,finance,telecommunication,etc..",
"required_languages":[{{"language": "Language name in English",
                       "proficiency":"Leave empty if not mentioned"}}],
"key_responsabilities":["task1","task2"],
"salary_range":"salary range if mentioned with the currency if not mentioned leave empty",
"location":"",
"category": "category_name"
}}

Please ensure that you ONLY return valid JSON. Do not include markdown formatting like ```json or ```.

Here is the job description:
\"\"\"{job_description_text}\"\"\"
    '''

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert assistant specialized in job description analysis."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1
    )

    result_text = chat_completion.choices[0].message.content.strip()

    result_text = re.sub(r"```json|```", "", result_text).strip()

    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse cleaned GPT response: {e}\nCleaned response was: {result_text}")


def extract_course_data(course_text: str) -> dict:
    """
    Analyse un texte de cours et en extrait les notions principales,
    sous forme structurée, pour servir ensuite à la génération de questions.
    """

    prompt = f"""
You are an academic content analyzer.  
Your task is to extract the **main learning elements** from a provided course text.  
You must identify all important **concepts, subtopics, learning objectives, examples, and relationships**.

Return the output as a **valid JSON** (no markdown, no text).

The goal is to summarize this course material into a structured, machine-usable format
that will later be used to generate comprehension or application-based test questions.

📘 Course Content:
\"\"\"{course_text}\"\"\"

Expected JSON format:
{{
  "course_title": "If a title is mentioned in the text, extract it; otherwise leave empty",
  "main_topics": ["Topic 1", "Topic 2", "Topic 3"],
  "subtopics": {{
     "Topic 1": ["Subtopic A", "Subtopic B"],
     "Topic 2": ["Subtopic C"]
  }},
  "key_concepts": ["concept1", "concept2", "concept3"],
  "important_definitions": [
      {{"term": "definition"}},
      {{"term": "definition"}}
  ],
  "examples": ["brief list of real-world or text examples"],
  "learning_objectives": [
      "objective1",
      "objective2"
  ],
  "difficulty_level": "beginner | intermediate | advanced"
}}

⚠️ Return ONLY valid JSON, no markdown.
"""

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are an expert in pedagogy and knowledge structuring."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = chat_completion.choices[0].message.content.strip()

    # Nettoyer d'éventuels délimiteurs JSON
    result_text = re.sub(r"```json|```", "", result_text).strip()

    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GPT response: {e}\nResponse:\n{result_text}")


def extract_course_intelligence(course_text: str) -> dict:
    prompt = f"""
You are a senior subject-matter expert and academic content analyst.

Your task is to extract a STRICT, STRUCTURED, and FACTUAL knowledge base
from the provided course content.

This output will be used as the ONLY source of truth
for generating certification exam questions.

==================================================
CRITICAL EXTRACTION RULES (ABSOLUTE)
==================================================

- DO NOT summarize loosely
- DO NOT generalize
- DO NOT invent or infer missing rules
- DO NOT use external knowledge
- ONLY extract what is explicitly stated in the course

If a value, rate, threshold, or rule is NOT present → DO NOT create it.

==================================================
WHAT YOU MUST EXTRACT
==================================================

1️⃣ COURSE METADATA
- Course domain (finance, accounting, taxation, economics, mixed)
- Year, version, or legal reference IF explicitly mentioned

2️⃣ MAIN TOPICS (MANDATORY)
For each main topic:
- Topic name
- Short description (based ONLY on the course)
- Explicit rules
- Numeric values (rates, thresholds, deductions)
- Conditions of application
- Formulas (if any)
- Explicit examples from the course (if present)

3️⃣ NUMERIC VALUES INDEX
- All rates
- All thresholds
- All fixed amounts
- Units and scope

4️⃣ EXPLICIT LIMITATIONS
- What the course DOES NOT define
- Missing rates or rules that must NOT be assumed

==================================================
OUTPUT FORMAT (STRICT JSON ONLY)
==================================================

{{
  "course_domain": "",
  "course_version_or_year": "",
  "main_topics": [
    {{
      "topic_name": "",
      "description": "",
      "rules": [
        {{
          "rule_type": "",
          "description": "",
          "values": {{}},
          "conditions": ""
        }}
      ],
      "formulas": [
        {{
          "name": "",
          "formula_expression": "",
          "variables_explained": {{}}
        }}
      ],
      "examples_if_any": []
    }}
  ],
  "explicit_values_index": {{
    "rates": [],
    "thresholds": [],
    "fixed_deductions": []
  }},
  "forbidden_assumptions": []
}}

==================================================
COURSE CONTENT
==================================================

\"\"\"{course_text}\"\"\"

Return ONLY valid JSON.
"""

    chat_completion = openai.ChatCompletion.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {"role": "system", "content": "You are an expert in pedagogy and knowledge structuring."},
            {"role": "user", "content": prompt}
        ]
    )

    result_text = chat_completion.choices[0].message.content.strip()

    # Nettoyer d'éventuels délimiteurs JSON
    result_text = re.sub(r"```json|```", "", result_text).strip()

    try:
        return json.loads(result_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse GPT response: {e}\nResponse:\n{result_text}")

