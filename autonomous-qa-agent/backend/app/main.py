# backend/app/main.py

from .rag import set_html_structure
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from .ingest_new import save_uploaded_file, extract_text_from_path, build_vector_store_from_texts
from .rag import generate_test_cases_from_prompt
from .generator import create_selenium_script


app = FastAPI(title="Autonomous QA Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOADED_DOCS = []
UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

HTML_PATH = "target_site/checkout.html"
if os.path.exists(HTML_PATH):
    set_html_structure(HTML_PATH)
    print(f"✓ HTML structure loaded from {HTML_PATH}")
else:
    print(f"⚠ Warning: {HTML_PATH} not found")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/upload_docs")
async def upload_docs(files: List[UploadFile] = File(...)):
    global UPLOADED_DOCS
    UPLOADED_DOCS = []

    paths = []
    for file in files:
        saved = await save_uploaded_file(file, UPLOAD_DIR)
        text = extract_text_from_path(saved)

        UPLOADED_DOCS.append({"filename": os.path.basename(saved), "text": text})
        paths.append(str(saved))

    return {"status": "uploaded", "files": paths}


@app.post("/build_kb")
def build_kb():
    if not UPLOADED_DOCS:
        return {"error": "Upload documents first"}

    added = build_vector_store_from_texts(UPLOADED_DOCS)
    return {"status": "kb_built", "added": added}


@app.post("/generate_tests")
def generate_tests(body: dict):
    prompt = body.get("prompt")
    if not prompt:
        return {"error": "prompt missing"}

    tests = generate_test_cases_from_prompt(prompt)
    return {"tests": tests}


@app.post("/generate_script")
def generate_script(test_case: dict):
    script = create_selenium_script(test_case)
    return {"script": script}
