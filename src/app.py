from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lomake")
def form():
    return render_template("lomake.html")

@app.route("/submit", methods=["POST"])
def submit():
    key = request.form["cite_key"]
    return key