from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse  
from app.services import pdf_parser, extractor, gpt_generator
from app.db.mongo import test_collection, jd_collection
import asyncio
from fastapi.responses import StreamingResponse
from fastapi import Request
import json
import re
import datetime
import os

router = APIRouter(
    tags=["Upload & Analyse"]
)

# ✅ Dossier Desktop pour stocker les tests
save_dir = os.path.expanduser("~/Desktop/generated_tests")
os.makedirs(save_dir, exist_ok=True)


# upload with SSE
@router.post("/upload-stream")
async def upload_stream(
    request: Request,
    file: UploadFile = File(...),
    seniority_input: str = Form(...),
    language_input: str = Form(...),
    number_of_questions: int = Form(30) 
):
    # read file content before le stream
    try:
        content = await file.read()
        print("Fichier lu avant stream (taille):", len(content))
    except Exception as e:
        return StreamingResponse(
            iter([f"data: Error reading file: {str(e)}\n\n"]),
            media_type="text/event-stream"
        )

    #fct qui recoit le fichier deja charge
    async def generate_events():
        try:
            yield "data: Uploading file...\n\n"

            yield "data: Extracting text from PDF...\n\n"
            text = pdf_parser.extract_text_from_pdf(content)
            print(" Début du texte extrait:", text[:100])

            yield "data: Analyzing course...\n\n"
            course_data = extractor.extract_course_data(text)
            # job_data = extractor.extract_job_data(text)

            print(" Données extraites:", course_data)

            jd_doc = {"raw_text": text, "extracted_data": course_data}
            jd_result = jd_collection.insert_one(jd_doc)
            jd_id = str(jd_result.inserted_id)

            yield f"data: Generating a {number_of_questions}-question test... Please wait...\n\n"
            generated_test = gpt_generator.generate_certification_test_from_course(
            # generated_test = gpt_generator.generate_test_from_job_description(
                text,
                seniority_input,
                number_of_questions,
                language_input
            )
            print(" test genere avec succees!!!!.")

            # save test on local (desktop)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
            file_name = f"test-{timestamp}.json"
            file_path = os.path.join(save_dir, file_name)

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump({
                    "test_id": jd_id,
                    # "test_id": None,
                    "seniority": seniority_input,
                    "language": language_input,
                    "num_questions": number_of_questions,
                    "generated_test": generated_test
                }, f, ensure_ascii=False, indent=2)

            print(f"✅ Test enregistré sur le Desktop : {file_path}")

            # Insert into MongoDB collection
            test_doc = {
                "test_id": jd_id,
                "test_data": generated_test,
                "seniority": seniority_input,
                "language": language_input,
                "num_questions": number_of_questions,
                "local_file_path": file_path
            }
            test_result = test_collection.insert_one(test_doc)
            test_id = str(test_result.inserted_id)

            result = {
                "test_id": jd_id,
                "extracted_job_data": course_data,
                "generated_test": generated_test,
                "local_file_path": file_path
                
            }

            yield f"data: __DONE__{json.dumps(result)}\n\n"

        except Exception as e:
            print("Exception dans generate_events():", str(e))
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(generate_events(), media_type="text/event-stream")

# upload without SSE
@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    seniority_input: str = Form(...),
    language_input: str = Form(...)
):
    content = await file.read()
    text = pdf_parser.extract_text_from_pdf(content)

    # Extraction job data
    job_data = extractor.extract_job_data(text)

    # Insert job description
    jd_doc = {
        "raw_text": text,
        "extracted_data": job_data
    }
    jd_result = jd_collection.insert_one(jd_doc)
    jd_id = str(jd_result.inserted_id)

    # generate test 
    generated_test = gpt_generator.generate_test_from_job_description(
        text,
        seniority_input=seniority_input,
        language_input=language_input
    )

    # Insert test
    test_doc = {
        "jd_id": jd_id,
        "test_data": generated_test,
        "seniority": seniority_input,
        "language": language_input
    }
    test_result = test_collection.insert_one(test_doc)
    test_id = str(test_result.inserted_id)

    return {
        "jd_id": jd_id,
        "test_id": test_id,
        "extracted_job_data": job_data,
        "generated_test": generated_test
    }

# get all generated tests 
@router.get("/tests")
async def get_all_tests():
    """
    🔍 Retourne la liste de tous les tests stockés dans MongoDB.
    """
    try:
        tests = list(test_collection.find())

        # Convertir ObjectId en string pour éviter les erreurs JSON
        for test in tests:
            test["_id"] = str(test["_id"])
            if "test_id" in test:
                test["test_id"] = str(test["test_id"])

        return JSONResponse(content={
            "count": len(tests),
            "tests": tests
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
    
""" 
@router.post("/upload-stream")
async def upload_stream(
    request: Request,
    file: UploadFile = File(...),
    seniority_input: str = Form(...),
    language_input: str = Form(...),
    number_of_questions: int = Form(30)
):
    content = await file.read()
    text = pdf_parser.extract_text_from_pdf(content)
    course_data = extractor.extract_course_data(text)

    jd_doc = {"raw_text": text, "extracted_data": course_data}
    jd_result = jd_collection.insert_one(jd_doc)
    jd_id = str(jd_result.inserted_id)

    async def generate_events():
        yield "data: Uploading file...\n\n"
        yield "data: Extracting text from PDF...\n\n"
        yield "data: Generating certification test...\n\n"

        question_count = 0
        generated_text = ""  # On accumule ici le JSON complet

        try:
            # ⚡ Boucle sur le générateur GPT
            for event in gpt_generator.generate_certification_test_from_course(
                text, seniority_input, number_of_questions, language_input
            ):
                # Progression à chaque question détectée
                if event == "progress":
                    question_count += 1
                    yield f"data: Generating question {question_count}/{number_of_questions}\n\n"
                    await asyncio.sleep(0.1)  # léger yield pour le flux

                # Fin de génération
                elif isinstance(event, tuple) and event[0] == "done":
                    generated_text = event[1]

            # 🧩 Nettoyage du texte JSON
            cleaned_text = re.sub(
                r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", generated_text, flags=re.MULTILINE
            ).strip()

            generated_test = json.loads(cleaned_text)

            # ✅ Insertion finale dans Mongo
            test_doc = {
                "jd_id": jd_id,
                "test_data": generated_test,
                "seniority": seniority_input,
                "language": language_input,
                "num_questions": number_of_questions
            }
            test_result = test_collection.insert_one(test_doc)
            test_id = str(test_result.inserted_id)

            result = {
                "jd_id": jd_id,
                "test_id": test_id,
                "extracted_course_data": course_data,
                "generated_test": generated_test
            }

            # Envoi final au front
            yield f"data: __DONE__{json.dumps(result)}\n\n"

        except Exception as e:
            print("Exception in generate_events():", str(e))
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(generate_events(), media_type="text/event-stream")
 """