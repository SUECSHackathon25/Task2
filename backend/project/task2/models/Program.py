from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db


class Program(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: MappedColumn[str] = mapped_column(String(length=200), nullable=False)
