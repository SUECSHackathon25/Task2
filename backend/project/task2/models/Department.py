from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db


class Department(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: MappedColumn[str] = mapped_column(String(length=200), nullable=False)
    
    def __str__(self):
        return f'{self.name}'