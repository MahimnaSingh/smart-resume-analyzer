# api/index.py  (UTF-8)
from flask import Flask, request, jsonify, Response
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB uploads

@app.get("/")
def root():
    return Response("Flask OK: runtime & routing work", mimetype="text/plain")

def extract_pdf_text(file_bytes: bytes) -> str:
    try:
        from PyPDF2 import PdfReader  # lazy import keeps cold start small
        reader = PdfReader(io.BytesIO(file_bytes))
        parts = []
        for p in reader.pages:
            try:
                parts.append(p.extract_text() or "")
            except Exception:
                pass
        return "\n".join(parts)
    except Exception as e:
        return f"[pdf-extract-error] {e}"

# lightweight keyword buckets; tweak as you like
SKILL_BUCKETS = {
    "python": ["python", "pandas", "numpy"],
    "data":   ["sql", "excel", "power bi", "tableau"],
    "ml":     ["scikit-learn", "machine learning", "regression", "classification"],
}

@app.post("/analyze")
def analyze():
    if "file" not in request.files:
        return jsonify(ok=False, error="missing 'file' field (multipart/form-data)"), 400

    f = request.files["file"]
    name = (f.filename or "").lower()
    blob = f.read()

    if name.endswith(".pdf"):
        text = extract_pdf_text(blob)
    elif name.endswith(".txt"):
        text = blob.decode("utf-8", "ignore")
    else:
        return jsonify(ok=False, error="Only .pdf or .txt supported"), 415

    low = (text or "").lower()
    scores = {bucket: sum(kw in low for kw in kws) for bucket, kws in SKILL_BUCKETS.items()}
    total = int(sum(scores.values()))
    return jsonify(ok=True, filename=name, scores=scores, total=total, preview=(text or "")[:800])
