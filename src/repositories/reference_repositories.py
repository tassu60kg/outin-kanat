from sqlalchemy import text
from config import db
def add_reference(**data):
    sql =  """
    INSERT INTO bib_references
        (cite_key, type, author, title, year,
         publisher, isbn, journal, booktitle, volume, pages)
    VALUES
        (:cite_key, :type, :author, :title, :year,
         :publisher, :isbn, :journal, :booktitle, :volume, :pages)"""
    db.session.execute(text(sql), data)
    db.session.commit()

def get_all():
    sql = sql = """SELECT * FROM bib_references
        ORDER BY id DESC"""
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_reference_by_id(reference_id):
    sql = "SELECT * FROM bib_references WHERE id = :id"
    result = db.session.execute(text(sql), {"id": reference_id})
    return result.fetchone()

def remove_reference(reference_id):
    sql = "DELETE FROM tags WHERE bib_reference = :id"
    db.session.execute(text(sql), {"id": reference_id})
    sql = "DELETE FROM bib_references WHERE id = :id"
    db.session.execute(text(sql), {"id": reference_id})
    db.session.commit()

def update_reference(**data):
    sql = """UPDATE bib_references SET cite_key=:cite_key,
        author=:author, title=:title, year=:year,
        publisher=:publisher, isbn=:isbn, journal=:journal,
        booktitle=:booktitle, volume=:volume, pages=:pages WHERE id=:id"""
    db.session.execute(text(sql), data)
    db.session.commit()

def add_tag(**data):
    sql = """INSERT INTO tags (bib_reference, tag) VALUES (:bib_reference, :tag)"""
    db.session.execute(text(sql), data)
    db.session.commit()

def get_all_tags():
    sql = "SELECT bib_reference, tag FROM tags"
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_tags(bib_reference):
    sql = """SELECT tag FROM tags WHERE bib_reference=:bib_reference"""
    result = db.session.execute(text(sql), {"bib_reference": bib_reference})
    return result.fetchall()

def delete_tag(**data):
    sql = """DELETE FROM tags WHERE tag=:tag"""
    db.session.execute(text(sql), data)
    db.session.commit()
