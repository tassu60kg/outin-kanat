from flask import Flask, redirect, render_template, request
import repositories.reference_repositories
from config import app, db
from util import validate_year

@app.route("/")
def index():
    sql = repositories.reference_repositories.get_all()
    print(sql)
    return render_template("index.html", sql=sql)

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

    try:
        validate_year(int(year))
        repositories.reference_repositories.add_book(key, author, title, year, publisher, ISBN)
    except Exception as error:
        raise Exception("Virheellinen vuosi: " + str(error))
    return redirect("/")