import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Film(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    comment = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sumRating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    countRating = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    addedBy = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    api_id = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=True)
    user = orm.relationship('User')