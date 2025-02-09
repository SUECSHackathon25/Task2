from sqlalchemy.orm import mapped_column, relationship, Relationship
from sqlalchemy import Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db
from task2.models.Poster import Poster
from task2.models.Judge import Judge

class Score(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    judge_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Judge.id), nullable=False)
    poster_id: MappedColumn[int] = mapped_column(Integer, ForeignKey(column=Poster.id), nullable=False)
    score : MappedColumn[int] = mapped_column(Integer, nullable=True)
    __table_args__: tuple[CheckConstraint] = (
        CheckConstraint(sqltext='Score BETWEEN 1 AND 10', name='check_score_range'), 
    ) 
    
    judge: Relationship[Judge] = relationship(argument=Judge, back_populates='scores')
    poster: Relationship[Poster] = relationship(argument=Poster, back_populates='scores')
