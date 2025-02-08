from sqlalchemy.orm import mapped_column, relationship, MappedColumn, Relationship
from sqlalchemy import ForeignKey, Integer, String
from task2.database import db
from task2.models.Judge import Judge
from task2.models.Program import Program

class Poster(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    title: MappedColumn[str] = mapped_column(String(length=200), nullable=False)
    abstract: MappedColumn[str] = mapped_column(String(length=500), nullable=False)
    advisor_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Judge.id), nullable=False)
    program_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Program.id), nullable=False)
    
    advisor: Relationship[Judge] = relationship(argument=Judge, backref='advisor')
    program: Relationship[Program] = relationship(argument=Program, backref='program')

    
# Title Abstract Advisor First Advisor Last Program