from flask import flash, redirect, render_template, request
import repositories.reference_repositories
from config import app
from util import validate_year

@app.route("/")
def index():
    references = repositories.reference_repositories.get_all()
    return render_template("index.html", reference = references)

@app.route("/add_reference")
def form():
    return render_template("add_reference.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    data = {
        "cite_key": request.form.get("cite_key"),
        "type": request.form.get("type"),
        "author": request.form.get("author"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "publisher": request.form.get("publisher"),
        "ISBN": request.form.get("ISBN"),
        "journal": request.form.get("journal"),
        "booktitle": request.form.get("booktitle"),
        "volume": request.form.get("volume"),
        "pages": request.form.get("pages"),
    }
    if "send" in request.form:
        validate_year(int(data["year"]))
        repositories.reference_repositories.add_reference(**data)
        return redirect("/")

    return redirect("/")

@app.route("/remove_reference/<int:reference_id>", methods=["GET", "POST"])
def remove_reference(reference_id):
    reference = repositories.reference_repositories.get_reference_by_id(reference_id)

    if request.method == "GET":
        return render_template("remove_reference.html", reference=reference)

    if request.method == "POST":
        if "remove" in request.form:
            repositories.reference_repositories.remove_reference(reference_id)
            flash("Reference removed successfully.")
            return redirect("/")

    return redirect("/")

@app.route("/update_reference/<int:reference_id>", methods=["GET", "POST"])
def update_reference(reference_id):
    reference = repositories.reference_repositories.get_reference_by_id(reference_id)

    if request.method == "GET":
        return render_template("update_reference.html", reference=reference)

    if request.method == "POST":
        data = {
        "cite_key": request.form.get("cite_key"),
        "type": request.form.get("type"),
        "author": request.form.get("author"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "publisher": request.form.get("publisher"),
        "ISBN": request.form.get("ISBN"),
        "journal": request.form.get("journal"),
        "booktitle": request.form.get("booktitle"),
        "volume": request.form.get("volume"),
        "pages": request.form.get("pages"),
        }
        if "update" in request.form:
            repositories.reference_repositories.update_reference(**data)
            flash("Reference updated successfully.")
            return redirect("/")

    return redirect("/")
