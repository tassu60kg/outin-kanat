import re

class UserInputError(Exception):
    pass

def validate_year(year):
    if not isinstance(year, int) or year < 0:
        raise UserInputError("Year must be a positive integer.")

def validate_cite_key(cite_key):
    if not isinstance(cite_key, str):
        raise UserInputError("Cite key must be text.")

    cite_key = cite_key.strip()

    if cite_key == "":
        raise UserInputError("Cite key cannot be empty.")

    if " " in cite_key:
        raise UserInputError("Cite key cannot contain spaces.")

    if not re.match(r"^[A-Za-z0-9_-]+$", cite_key):
        raise UserInputError("Cite key may only contain letters, numbers, hyphens and underscores.")

def generate_bibtex(ref):
    cite_key = ref["cite_key"]
    ref_type = ref["type"]

    fields = []

    def add_field(name, value):
        if value is not None and value != "":
            fields.append(f"  {name} = {{{value}}}")

    add_field("author", ref.get("author"))
    add_field("title", ref.get("title"))
    add_field("year", ref.get("year"))
    add_field("publisher", ref.get("publisher"))
    add_field("journal", ref.get("journal"))
    add_field("booktitle", ref.get("booktitle"))
    add_field("volume", ref.get("volume"))
    add_field("pages", ref.get("pages"))
    add_field("isbn", ref.get("isbn"))

    fields_block = ",\n".join(fields)

    return f"@{ref_type}{{{cite_key},\n{fields_block}\n}}"
