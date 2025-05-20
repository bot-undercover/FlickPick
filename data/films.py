import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Film(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="question.jpg")
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    date = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    sumRating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    countRating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    addedBy = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')