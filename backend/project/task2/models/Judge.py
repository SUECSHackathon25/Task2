from typing import Any
from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db


class Judge(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name= mapped_column(String(50), nullable=False)
