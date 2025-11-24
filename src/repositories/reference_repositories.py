from sqlalchemy import text
from config import db

def add_book(cite_key, author, title, year, publisher, ISBN):
    sql_insert =  """INSERT INTO bib_references
        (cite_key, type, author, title, year, publisher, ISBN,
        booktitle, journal, volume, pages)
        VALUES
        (:cite_key, :type, :author, :title, :year, :publisher, :ISBN,
         NULL, NULL, NULL, NULL)"""
    db.session.execute(text(sql_insert), { "type": "book",  "cite_key": cite_key, "author": author,
                                          "title": title, "year": year,
                                          "publisher": publisher, "ISBN": ISBN})
    db.session.commit()

def get_all():
    sql_insert = """SELECT *
              FROM bib_references"""
    result = db.session.execute(text(sql_insert))
    return result.fetchall()

def get_reference_by_id(reference_id):
    sql = "SELECT * FROM bib_references WHERE id = :id"
    result = db.session.execute(text(sql), {"id": reference_id})
    return result.fetchone()

def remove_reference(reference_id):
    sql = "DELETE FROM bib_references WHERE id = :id"
    db.session.execute(text(sql), {"id": reference_id})
    db.session.commit()
