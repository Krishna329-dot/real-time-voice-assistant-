from flask import Flask, send_from_directory
import webbrowser
import threading
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AVATAR_DIR = os.path.join(BASE_DIR, "avatar")

@app.route("/")
def index():
    return send_from_directory(AVATAR_DIR, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(AVATAR_DIR, path)

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1.0, open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
