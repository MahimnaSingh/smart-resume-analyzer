# api/index.py
from flask import Flask, request, jsonify, Response
import io
from PyPDF2 import PdfReader

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

@app.get("/")
def health():
    return Response("Flask OK: runtime & routing work", mimetype="text/plain")

@app.post("/analyze")
def analyze():
    if "file" not in request.files:
        return jsonify(ok=False, error="missing 'file' field"), 400
    f = request.files["file"]
    name = (f.filename or "").lower()
    blob = f.read()

    if name.endswith(".pdf"):
        reader = PdfReader(io.BytesIO(blob))
        text = "\n".join([(p.extract_text() or "") for p in reader.pages])
    elif name.endswith(".txt"):
        text = blob.decode("utf-8", "ignore")
    else:
        return jsonify(ok=False, error="Only .pdf or .txt supported"), 415

    low = (text or "").lower()
    scores = {
        "python": sum(kw in low for kw in ["python","pandas","numpy"]),
        "data":   sum(kw in low for kw in ["sql","excel","power bi","tableau"]),
        "ml":     sum(kw in low for kw in ["scikit-learn","machine learning","regression","classification"]),
    }
    return jsonify(ok=True, filename=name, scores=scores, total=int(sum(scores.values())), preview=(text or "")[:800])
