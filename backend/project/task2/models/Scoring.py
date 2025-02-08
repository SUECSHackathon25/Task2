from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String, CheckConstraint
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db
from task2.models.Poster import Poster
from task2.models.Judge import Judge

class Scoring(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    judge_id: MappedColumn[int] = mapped_column(Integer, nullable=False)
    poster_id: MappedColumn[int] = mapped_column(Integer, nullable=False)
    score = MappedColumn[int] = mapped_column(Integer, nullable=True)
    __table_args__ = (
        CheckConstraint('Score BETWEEN 1 AND 10', name='check_score_range'), 
    ) 
    
    judge = relationship(Judge, backref='judge')
    poster = relationship(Judge, backref='poster')
    