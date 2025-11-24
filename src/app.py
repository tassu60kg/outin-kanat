from flask import redirect, render_template, request
import repositories.reference_repositories
from config import app
from util import validate_year

@app.route("/")
def index():
    references = repositories.reference_repositories.get_all()
    return render_template("index.html", reference = references)

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
    except ValueError as error:
        raise ValueError("Virheellinen vuosi: " + str(error)) from error
    return redirect("/")
