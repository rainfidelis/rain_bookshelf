from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from decouple import config


database_name = config('DATABASE_NAME')
database_user = config('DATABASE_USER')
database_password = config('DATABASE_PASSWORD')
database_host = config('DATABASE_HOST')
database_port = config('DATABASE_PORT')
# database_path = "postgresql://{}:{}@{}:{}/{}".format(
#     database_user, database_password, database_host, database_port,
#     database_name)

database_path = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
    database_user, database_password, database_host, database_port,
    database_name) # Use PG8000 as connector instead of psycopg2

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    """Binds a flask application and a SQLAlchemy service"""
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Book(db.Model):
    """Creates a book object in the database."""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, unique=True)
    title = Column(String)
    author = Column(String)
    rating = Column(Integer)

    def __init__(self, title, author, rating):
        self.title = title
        self.author = author
        self.rating = rating

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "rating": self.rating,
        }
