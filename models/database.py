from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

engine = create_engine('mysql://user:pwd@host:port/db_name')
session = engine.connect()


db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'my_part'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)


