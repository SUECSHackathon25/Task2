from typing import Any, List
from sqlalchemy.orm import mapped_column, relationship, Session, Relationship
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm.properties import MappedColumn
from sqlalchemy.orm.relationships import _RelationshipDeclared
from task2.database import db
from task2.models.Department import Department
from task2.models.User import User


class Judge(db.Model):
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True)
    first_name: MappedColumn[str] = mapped_column(String(length=50), nullable=False)
    last_name: MappedColumn[str] = mapped_column(String(length=50), nullable=False)
    department_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('department.id'), nullable=False) 
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey('app_user.id'), nullable=False)  
    
    # Relationships
    user = relationship("User", backref='judges') 
    department= relationship("Department", backref='judges') 
    scores = relationship('Score', back_populates='judge')
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_posters(self):
        print(self.scores)
    
