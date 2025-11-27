from fastapi import FastAPI
from app.routers import upload, submit, mock
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Job Test Generator API",
    description="API pour générer des tests techniques à partir de Job Description en PDF",
    version="1.0"
)

origins = [
    "http://localhost:53947",  
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:53947"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to Job Test Generator"}
app.include_router(upload.router, prefix="/api")
app.include_router(submit.router, prefix="/api")
app.include_router(mock.router, prefix="/api")  