from sqlalchemy import text
from config import db
def add_reference(**data):
    sql =  """
    INSERT INTO bib_references
        (cite_key, type, author, title, year,
         publisher, ISBN, journal, booktitle, volume, pages)
    VALUES
        (:cite_key, :type, :author, :title, :year,
         :publisher, :ISBN, :journal, :booktitle, :volume, :pages)"""
    db.session.execute(text(sql), data)
    db.session.commit()

def get_all():
    sql = """SELECT *
              FROM bib_references"""
    result = db.session.execute(text(sql))
    return result.fetchall()

def get_reference_by_id(reference_id):
    sql = "SELECT * FROM bib_references WHERE id = :id"
    result = db.session.execute(text(sql), {"id": reference_id})
    return result.fetchone()

def remove_reference(reference_id):
    sql = "DELETE FROM bib_references WHERE id = :id"
    db.session.execute(text(sql), {"id": reference_id})
    db.session.commit()

def update_reference(**data):
    sql = """UPDATE bib_references SET cite_key=:cite_key, type=:type,
        author=:author, title=:title, year=:year,
        publisher=:publisher, ISBN=:ISBN, journal=:journal,
        booktitle=:booktitle, volume=:volume, pages=:pages"""
    db.session.execute(text(sql), data)
    db.session.commit()
