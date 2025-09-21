# api/index.py  — minimal, defensive Flask API for Vercel
from flask import Flask, request, jsonify, Response
from werkzeug.exceptions import RequestEntityTooLarge
import io

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10 MB

@app.get("/")
def health():
    # text/plain on purpose so you can eyeball it in the browser
    return Response("Flask OK: runtime & routing work", mimetype="text/plain")

@app.get("/ping")
def ping():
    # quick JSON probe endpoint
    return jsonify(ok=True, status="up")

def extract_pdf_text(b: bytes) -> str:
    try:
        from PyPDF2 import PdfReader  # lazy import keeps cold start small
        reader = PdfReader(io.BytesIO(b))
        return "\n".join([(p.extract_text() or "") for p in reader.pages])
    except Exception as e:
        return f"[pdf-extract-error] {e}"

@app.post("/analyze")
def analyze():
    try:
        if "file" not in request.files:
            return jsonify(ok=False, error="missing 'file' field (multipart/form-data)"), 400

        f = request.files["file"]
        filename = (f.filename or "").lower()
        blob = f.read() or b""

        if not filename:
            return jsonify(ok=False, error="filename is required"), 400

        if filename.endswith(".pdf"):
            text = extract_pdf_text(blob)
        elif filename.endswith(".txt"):
            try:
                text = blob.decode("utf-8", "ignore")
            except Exception as e:
                return jsonify(ok=False, error=f"txt decode error: {e}"), 415
        else:
            return jsonify(ok=False, error="Only .pdf or .txt supported"), 415

        low = (text or "").lower()
        scores = {
            "python": sum(kw in low for kw in ["python", "pandas", "numpy"]),
            "data":   sum(kw in low for kw in ["sql", "excel", "power bi", "tableau"]),
            "ml":     sum(kw in low for kw in ["scikit-learn", "machine learning", "regression", "classification"]),
        }
        total = int(sum(scores.values()))
        return jsonify(ok=True, filename=filename, scores=scores, total=total, preview=(text or "")[:800])

    except RequestEntityTooLarge:
        return jsonify(ok=False, error="File too large (max 10 MB)"), 413
    except Exception as e:
        # FINAL safety net: client will *always* see JSON
        return jsonify(ok=False, error=f"server error: {type(e).__name__}: {e}"), 500
