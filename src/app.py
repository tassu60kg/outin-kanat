from flask import flash, redirect, render_template, request
import requests
import repositories.reference_repositories
from config import app
from util import validate_year

@app.route("/")
def index():
    references = repositories.reference_repositories.get_all()
    tags = repositories.reference_repositories.get_all_tags()

    unique_tags = {tag.tag: tag for tag in tags}.values()

    selected_tags = request.args.getlist("tags")

    if selected_tags:
        references = repositories.reference_repositories.filter_references_by_tags(selected_tags)

    return render_template("index.html", reference=references, tag=tags, unique_tags=unique_tags)

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
        return render_template("create_bibtex.html", references=references)
    if request.method == "POST":
        return redirect("/")
    return redirect("/")

def fetch_reference_by_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        return None

    data = response.json()
    item = data['message']

    year = (item.get("published-print", {}).get("date-parts", [[None]])[0][0] or
            item.get("published-online", {}).get("date-parts", [[None]])[0][0])

    authors = ", ".join([f"{a.get('given', '')} {a.get('family', '')}".strip()
                        for a in item.get("author", [])])

    container_title = item.get("container-title")[0] if item.get("container-title") else None

    reference_type = item.get("type", "")

    if reference_type == "journal-article":
        data = {
        "cite_key": generate_cite_key(authors, year),
        "type": "article",
        "author": authors,
        "title": item.get("title")[0],
        "year": year,
        "publisher": None,
        "journal": container_title,
        "booktitle": None,
        "volume": item.get("volume"),
        "pages": item.get("page", "").replace("-", "–"),
        "isbn": None
        }
        return data

    if reference_type == "book":
        isbn = item.get("ISBN")[0] if item.get("ISBN") else None
        data = {
        "cite_key": generate_cite_key(authors, year),
        "type": "book",
        "author": authors,
        "title": item.get("title")[0],
        "year": year,
        "publisher": item.get("publisher"),
        "journal": None,
        "booktitle": None,
        "volume": None,
        "pages": None,
        "isbn": isbn
        }
        return data

    if reference_type in ["proceedings-article", "conference-paper"]:
        data = {
        "cite_key": generate_cite_key(authors, year),
        "type": "inproceedings",
        "author": authors,
        "title": item.get("title")[0],
        "year": year,
        "publisher": None,
        "journal": None,
        "booktitle": container_title if container_title else "Unknown Conference Proceedings",
        "volume": None,
        "pages": None,
        "isbn": None
        }
        return data
    return flash("Unknown reference type! Must be article, book, or inproceedings.")

@app.route("/add_reference_with_doi", methods=["GET", "POST"])
def add_reference_with_doi():
    if "back" in request.form:
        return redirect("/")

    if request.method == "GET":
        return render_template("add_reference_with_doi.html")

    if "send" in request.form:
        doi = request.form.get("doi")
        data = fetch_reference_by_doi(doi)

        if not data:
            flash("No Data was found with this DOI. Please check it and try again.")
            return redirect("/add_reference_with_doi")

        exists = repositories.reference_repositories.add_reference(**data)

        if not exists:
            flash("Reference already exists!")
            return redirect("/add_reference_with_doi")
        flash("Reference added successfully!")
        return redirect("/")

    if request.method == "POST":
        return redirect("/")

    return redirect("/")

def generate_cite_key(authors, year):
    if not authors:
        return f"Anon{year}"

    author_list = [a.strip() for a in authors.split(",") if a.strip()]
    if not author_list:
        return f"Anon{year}"

    if len(author_list) == 1:
        last_name = author_list[0].split()[-1]
        return f"{last_name}{str(year)[-2:]}"

    letters = "".join(name.split()[-1][0] for name in author_list)
    return f"{letters}{str(year)[-2:]}"
