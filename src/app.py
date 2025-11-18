from flask import Flask, render_template, request
import repositories.reference_repositories
from config import app, db

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/lomake")
def form():
    return render_template("lomake.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    key = request.form["cite_key"]
    author = request.form["author"]
    title = request.form["title"]
    year = request.form["year"]
    publisher = request.form["publisher"]
    ISBN = request.form["ISBN"]
    repositories.reference_repositories.add_book(key, author, title, year, publisher, ISBN)
    return render_template("index.html")