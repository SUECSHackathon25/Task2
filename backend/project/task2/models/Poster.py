from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer
from task2.database import db


class Poster(db.Model):
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
