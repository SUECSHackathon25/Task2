from sqlalchemy.orm import mapped_column, relationship, MappedColumn, Relationship
from sqlalchemy import ForeignKey, Integer, String
from task2.database import db
from task2.models.Judge import Judge
from task2.models.Program import Program

class Poster(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    title: MappedColumn[str] = mapped_column(String(length=400), nullable=False)
    abstract: MappedColumn[str] = mapped_column(String(length=5000), nullable=False)
    advisor_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Judge.id), nullable=True)
    program_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Program.id), nullable=False)
    
    advisor: Relationship[Judge] = relationship(argument=Judge, backref='advisor')
    program: Relationship[Program] = relationship(argument=Program, backref='program')
    scores = relationship('Score', back_populates='poster')


# Title Abstract Advisor First Advisor Last Program