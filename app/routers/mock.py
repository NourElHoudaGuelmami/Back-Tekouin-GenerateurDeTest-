from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/mock",
    tags=["Mock Data"]
)

@router.get("/generated-test")
async def get_mock_generated_test():
    mock_test = {
        "generated_test": {
            "title": "Frontend Developer Assessment",
            "estimated_total_time_minutes": 30,
            "total_time_limit_minutes": 30,
            "questions": [
                {
                    "id": 1,
                    "category": "Angular Fundamentals",
                    "question": "Which Angular decorator is used to define a component?",
                    "choices": {
                        "A": "@Injectable()",
                        "B": "@NgModule()",
                        "C": "@Component()",
                        "D": "@Directive()"
                    },
                    "correct_answer": "C",
                    "explanation": "The @Component decorator marks a class as an Angular component.",
                },
                {
                    "id": 2,
                    "category": "TypeScript",
                    "question": "What is the correct way to define an interface in TypeScript?",
                    "choices": {
                        "A": "interface Person { name: string; age: number; }",
                        "B": "define Person { name: string; age: number; }",
                        "C": "class Person { name: string; age: number; }",
                        "D": "let Person = { name: string; age: number; }"
                    },
                    "correct_answer": "A",
                    "explanation": "Interfaces in TypeScript are declared with the 'interface' keyword.",
                },
                {
                    "id": 3,
                    "category": "Angular Components",
                    "question": "Which lifecycle hook is called when a component is initialized?",
                    "choices": {
                        "A": "ngAfterViewInit",
                        "B": "ngOnInit",
                        "C": "ngOnChanges",
                        "D": "ngDestroy"
                    },
                    "correct_answer": "B",
                    "explanation": "ngOnInit() is called once after the component is initialized.",
                },
                {
                    "id": 4,
                    "category": "HTML & CSS",
                    "question": "What CSS property controls text size?",
                    "choices": {
                        "A": "font-style",
                        "B": "font-size",
                        "C": "text-size",
                        "D": "text-style"
                    },
                    "correct_answer": "B",
                    "explanation": "The 'font-size' property defines the size of the text.",
                },
                {
                    "id": 5,
                    "category": "JavaScript",
                    "question": "Which of the following is a valid way to declare a variable in ES6?",
                    "choices": {
                        "A": "var myVar = 10;",
                        "B": "let myVar = 10;",
                        "C": "const myVar = 10;",
                        "D": "Both B and C"
                    },
                    "correct_answer": "D",
                    "explanation": "ES6 introduced 'let' and 'const' for block-scoped variables.",
                }
            ]
        }
    }
    return JSONResponse(content=mock_test)

@router.get("/test-result")
async def get_mock_test_result():
    mock_result = {
        "total_score": 85,
        "score_percent": 85.0,
        "pass_score_required": 70,
        "status": "Passed",
        "details": [
            {
                "question": "Which Angular decorator is used to define a component?",
                "selected_answer": "C",
                "correct_answer": "C",
                "is_correct": True,
                "score_awarded": 10
            },
            {
                "question": "What is the correct way to define an interface in TypeScript?",
                "selected_answer": "A",
                "correct_answer": "A",
                "is_correct": True,
                "score_awarded": 10
            },
            {
                "question": "Which lifecycle hook is called when a component is initialized?",
                "selected_answer": "B",
                "correct_answer": "B",
                "is_correct": True,
                "score_awarded": 10
            },
            {
                "question": "What CSS property controls text size?",
                "selected_answer": "B",
                "correct_answer": "B",
                "is_correct": True,
                "score_awarded": 10
            },
            {
                "question": "Which of the following is a valid way to declare a variable in ES6?",
                "selected_answer": "C",
                "correct_answer": "D",
                "is_correct": False,
                "score_awarded": 0
            }
        ]
    }
    return JSONResponse(content=mock_result)

from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/mock",
    tags=["Mock Data"]
)

# ==========================================================
# 1️⃣ MOCK : génération du test (simulate /upload-stream)
# ==========================================================
@router.get("/generated-test")
async def get_mock_generated_test():
    mock_test = {
        "generated_test": {
            "job_title": "Frontend Developer",
            "language": "English",
            "estimated_total_time_minutes": 20,
            "total_time_limit_minutes": 25,
            "questions": [
                {
                    "id": 1,
                    "category": "Angular Fundamentals",
                    "question": "Which decorator defines a component in Angular?",
                    "choices": {"A": "@Injectable", "B": "@Directive", "C": "@Component", "D": "@NgModule"},
                    "correct_answer": "C",
                    "explanation": "The @Component decorator identifies a class as an Angular component.",
                },
                {
                    "id": 2,
                    "category": "Angular Fundamentals",
                    "question": "Which file typically contains the root Angular module?",
                    "choices": {"A": "main.ts", "B": "app.module.ts", "C": "index.html", "D": "angular.json"},
                    "correct_answer": "B",
                    "explanation": "The root module of an Angular app is usually defined in app.module.ts.",
                }    ,

                # --- TypeScript (5)
                {
                    "id": 6,
                    "category": "TypeScript",
                    "question": "Which keyword is used to define an interface in TypeScript?",
                    "choices": {"A": "type", "B": "interface", "C": "define", "D": "class"},
                    "correct_answer": "B",
                    "explanation": "Interfaces are declared using the 'interface' keyword.",
                },
             
                {
                    "id": 8,
                    "category": "TypeScript",
                    "question": "Which feature allows defining multiple possible types for a variable?",
                    "choices": {"A": "Type assertion", "B": "Union types", "C": "Type inference", "D": "Interfaces"},
                    "correct_answer": "B",
                    "explanation": "Union types (using '|') allow multiple possible types.",
                },

                # --- RxJS & Observables (5)
                {
                    "id": 11,
                    "category": "RxJS & Observables",
                    "question": "Which operator is used to transform each emitted value of an Observable?",
                    "choices": {"A": "filter", "B": "map", "C": "merge", "D": "take"},
                    "correct_answer": "B",
                    "explanation": "The 'map' operator transforms emitted items.",
                },

                # --- HTML & CSS (5)
                {
                    "id": 16,
                    "category": "HTML & CSS",
                    "question": "Which HTML tag is used to include external JavaScript files?",
                    "choices": {"A": "<style>", "B": "<script>", "C": "<link>", "D": "<js>"},
                    "correct_answer": "B",
                    "explanation": "The <script> tag includes or embeds JavaScript in HTML.",
                },

                # --- JavaScript ES6+ (5)
                {
                    "id": 21,
                    "category": "JavaScript ES6+",
                    "question": "Which keyword declares a block-scoped variable?",
                    "choices": {"A": "var", "B": "let", "C": "const", "D": "Both B and C"},
                    "correct_answer": "D",
                    "explanation": "ES6 introduced 'let' and 'const' for block scoping.",
                },
                {
                    "id": 22,
                    "category": "JavaScript ES6+",
                    "question": "Which method converts a JSON string to an object?",
                    "choices": {"A": "JSON.parse()", "B": "JSON.stringify()", "C": "Object.create()", "D": "parseJSON()"},
                    "correct_answer": "A",
                    "explanation": "JSON.parse() parses a JSON string into an object.",
                },


                # --- Angular Advanced Topics (5)
                {
                    "id": 26,
                    "category": "Angular Advanced Topics",
                    "question": "Which decorator is used for dependency injection in a component?",
                    "choices": {"A": "@Inject", "B": "@Optional", "C": "@Input", "D": "@Output"},
                    "correct_answer": "A",
                    "explanation": "@Inject allows specifying a dependency to be injected manually.",
                },
                {
                    "id": 30,
                    "category": "Angular Advanced Topics",
                    "question": "Which Angular feature allows prefetching data before route activation?",
                    "choices": {"A": "Guards", "B": "Resolvers", "C": "Interceptors", "D": "Providers"},
                    "correct_answer": "B",
                    "explanation": "Resolvers fetch data before navigating to a route.",
                }
            ]
        }
    }
    return JSONResponse(content=mock_test)

# ==========================================================
# 2️⃣ MOCK : soumission du test (simulate /submit-test)
# ==========================================================
@router.post("/submit-test")
async def mock_submit_test():
    mock_result = {
        "total_score": 80,
        "score_percent": 80.0,
        "pass_score_required": 70,
        "status": "Passed",
        "details": [
            {"question": "Which Angular decorator is used to define a component?", "selected_answer": "A", "correct_answer": "A", "is_correct": True, "score_awarded": 10},
            {"question": "What is the correct way to define an interface in TypeScript?", "selected_answer": "B", "correct_answer": "B", "is_correct": True, "score_awarded": 10},
            {"question": "Which RxJS operator is used to transform the items emitted by an observable?", "selected_answer": "C", "correct_answer": "B", "is_correct": False, "score_awarded": 0},
            {"question": "Which module is required to use Angular routing?", "selected_answer": "C", "correct_answer": "C", "is_correct": True, "score_awarded": 10},
            {"question": "Which strategy minimizes unnecessary DOM updates?", "selected_answer": "B", "correct_answer": "B", "is_correct": True, "score_awarded": 10}
        ],
        # Simule le déclenchement immédiat de l’analyse comportementale
        "behavior_analysis": {
            "summary": "The candidate showed high consistency and fast responses, with only one hesitation detected.",
            "recommendations": "Encourage deeper understanding of RxJS transformations. Overall performance indicates solid Angular knowledge.",
            "questions_analysis": [
                {"question_index": 0, "suspicious": False, "reason": "confident"},
                {"question_index": 1, "suspicious": False, "reason": "steady"},
                {"question_index": 2, "suspicious": True, "reason": "hesitation"},
                {"question_index": 3, "suspicious": False, "reason": "fast"},
                {"question_index": 4, "suspicious": False, "reason": "confident"}
            ]
        }
    }
    return JSONResponse(content=mock_result)

# ==========================================================
# 3️⃣ MOCK : analyse comportementale seule (/analyze-behavior)
# ==========================================================
@router.get("/analyze-behavior")
async def get_mock_behavior_analysis():
    mock_behavior = {
        "summary": "The candidate showed steady confidence, with minor overthinking on 2 questions.",
        "recommendations": "Encourage faster decision-making in complex reasoning tasks. Candidate demonstrates strong technical consistency overall.",
        "questions_analysis": [
            {"question_index": 0, "suspicious": False, "reason": "confident"},
            {"question_index": 1, "suspicious": False, "reason": "steady"},
            {"question_index": 2, "suspicious": True, "reason": "overthinking"},
            {"question_index": 3, "suspicious": False, "reason": "fast"},
            {"question_index": 4, "suspicious": False, "reason": "confident"}
        ]
    }
    return JSONResponse(content=mock_behavior)
