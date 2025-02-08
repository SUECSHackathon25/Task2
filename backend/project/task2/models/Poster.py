from sqlalchemy.orm import mapped_column, relationship, Session, MappedColumn
from sqlalchemy import Integer, String
from task2.database import db
from task2.models.Judge import Judge
from task2.models.Program import Program

class Poster(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    title: MappedColumn[str] = mapped_column(String(length=200), nullable=False)
    abstract: MappedColumn[str] = mapped_column(String(length=500), nullable=False)
    advisor_id: MappedColumn[int] = mapped_column(Integer, nullable=False)
    program_id: MappedColumn[int] = mapped_column(Integer, nullable=False)
    
    advisor = relationship(Judge, backref='advisor')
    program = relationship(Program, backref='program')

    
# Title Abstract Advisor First Advisor Last Program