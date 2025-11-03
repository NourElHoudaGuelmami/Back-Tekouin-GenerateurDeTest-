import os
from dotenv import load_dotenv
import openai
import json
import re

# load_dotenv()


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


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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
