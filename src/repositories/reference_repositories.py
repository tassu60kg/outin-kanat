from config import db
from sqlalchemy import text

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