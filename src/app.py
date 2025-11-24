from flask import flash, redirect, render_template, request
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

@app.route("/remove_reference/<int:reference_id>", methods=["GET", "POST"])
def remove_reference(reference_id):

    reference = repositories.reference_repositories.get_reference_by_id(reference_id)

    if request.method == "GET":
        return render_template("remove_reference.html", reference=reference)
    
    if request.method == "POST":
        if "remove" in request.form:
            repositories.reference_repositories.remove_reference(reference_id)
            flash("Viite poistettu onnistuneesti")
            return redirect("/")
        
        elif "back" in request.form:
            return redirect("/")
