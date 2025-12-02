from flask import flash, redirect, render_template, request
import repositories.reference_repositories
from config import app
from util import validate_year

@app.route("/")
def index():
    references = repositories.reference_repositories.get_all()
    tags = repositories.reference_repositories.get_all_tags()
    return render_template("index.html", reference = references, tag = tags)

@app.route("/add_reference")
def form():
    return render_template("add_reference.html")

@app.route("/submit", methods=["POST", "GET"])
def submit():
    selected_type = request.form.get("type")

    if "back_to_home" in request.form:
        return redirect("/")

    if "back" in request.form:
        return render_template("add_reference.html", ref_type=None)

    if "send" not in request.form:
        return render_template("add_reference.html", ref_type=selected_type)

    data = {
        "cite_key": request.form.get("cite_key"),
        "type": request.form.get("type"),
        "author": request.form.get("author"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "publisher": request.form.get("publisher"),
        "isbn": request.form.get("isbn"),
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
            flash("Reference removed successfully!")
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
        "author": request.form.get("author"),
        "title": request.form.get("title"),
        "year": request.form.get("year"),
        "publisher": request.form.get("publisher"),
        "isbn": request.form.get("isbn"),
        "journal": request.form.get("journal"),
        "booktitle": request.form.get("booktitle"),
        "volume": request.form.get("volume"),
        "pages": request.form.get("pages"),
        "id": reference_id
        }
        if "update" in request.form:
            repositories.reference_repositories.update_reference(**data)
            flash("Reference updated successfully!")
            return redirect("/")

    return redirect("/")

@app.route("/update_tags/<int:reference_id>", methods=["GET", "POST"])
def update_tags(reference_id):
    reference = repositories.reference_repositories.get_reference_by_id(reference_id)
    tags = repositories.reference_repositories.get_tags(reference_id)

    if "back" in request.form:
        return redirect("/")

    if request.method == "GET":
        return render_template("update_tags.html", reference=reference, tags=tags)

    if request.method == "POST":
        data = {
            "tag": request.form.get("tag"),
            "bib_reference": request.form.get("bib_reference")
        }
        if "update" in request.form:
            repositories.reference_repositories.add_tag(**data)
            flash("Tags updated successfully!")
            return redirect(f"/update_tags/{reference_id}")
        if "delete" in request.form:
            repositories.reference_repositories.delete_tag(**data)
            flash("Tag removed successfully!")
            return redirect(f"/update_tags/{reference_id}")
    return redirect("/")

@app.route("/create_bibtex", methods=["GET", "POST"])
def create_bibtex():
    references = repositories.reference_repositories.get_all()
    if request.method == "GET":
        return render_template("create_bibtex.html", references = references)
    if request.method == "POST":
        return redirect("/")
    return redirect("/")
