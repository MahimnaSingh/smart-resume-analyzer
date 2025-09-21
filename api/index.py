from flask import Flask, Response
app = Flask(__name__)
@app.get("/")
def root():
    return Response("Flask OK", mimetype="text/plain")
