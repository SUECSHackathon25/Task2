from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db
from task2.models import Department


class Judge(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name= mapped_column(String(50), nullable=False)
    last_name= mapped_column(String(50), nullable=False)
    department_id = mapped_column(Integer, nullable=False)
    department = relationship(Department, backref='department')
    
