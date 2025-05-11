import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
import qrcode
from io import BytesIO
import base64
import requests

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        resp = requests.post(f"{API_BASE}/events/", json={"name": name})
        code = resp.json()["code"]
        return redirect(url_for("dashboard", code=code))
    return render_template("index.html")

@app.route("/dashboard/<code>")
def dashboard(code):
    evt = requests.get(f"{API_BASE}/events/{code}").json()
    link = f"{request.url_root}guest/{code}"
    img = qrcode.make(link)
    buf = BytesIO()
    img.save(buf)
    data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    return render_template("dashboard.html", code=code, name=evt["name"], qr=data_uri)

@app.route("/guest/<code>")
def guest(code):
    return render_template("guest.html", code=code)

@app.route("/api/events/<code>")
def proxy_event(code):
    r = requests.get(f"{API_BASE}/events/{code}")
    return jsonify(r.json())

@app.route("/api/search")
def proxy_search():
    q = request.args.get("q","")
    r = requests.get(f"{API_BASE}/search/", params={"q": q})
    return jsonify(r.json())

@app.route("/api/items/add", methods=["POST"])
def proxy_add():
    data = request.json
    r = requests.post(f"{API_BASE}/events/{data['code']}/items/", json=data["item"])
    return jsonify(r.json())

@app.route("/api/items/vote", methods=["POST"])
def proxy_vote():
    data = request.json
    r = requests.post(f"{API_BASE}/items/{data['id']}/vote")
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
