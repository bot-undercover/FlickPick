import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    picture = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="guest.png")
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    isAdmin = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    ratingSum = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    ratingCount = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=1)
    filmsRating = sqlalchemy.Column(sqlalchemy.String, nullable=True, default="")
    hashedPassword = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    banned = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True, default=False)
    creationDate = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    cookie = sqlalchemy.Column(sqlalchemy.String, nullable=True)