from sqlalchemy.orm import mapped_column, relationship, Session
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm.properties import MappedColumn
from task2.database import db


class User(db.Model):
    __tablename__ = "app_user"
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: MappedColumn[str] = mapped_column(String(length=200), nullable=False)
    admin: MappedColumn[bool] = mapped_column(Boolean, default=False)
