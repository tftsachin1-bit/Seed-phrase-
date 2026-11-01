"""Seed Phrase Generator website (Flask).

The server only serves the page and the public 2048-word list.
Phrases are generated and checked in the browser (JavaScript) and
never sent to the server.
"""
from flask import Flask, jsonify, send_from_directory

from bip39 import WORDS

app = Flask(__name__, static_folder="static", static_url_path="/static")


@app.after_request
def secure(resp):
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'none'; script-src 'self'; style-src 'self'; "
        "connect-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'none'"
    )
    return resp


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/wordlist.json")
def wordlist():
    return jsonify(WORDS)


if __name__ == "__main__":
    # 127.0.0.1 = only this computer can open it.
    app.run(host="127.0.0.1", port=5000, debug=False)
