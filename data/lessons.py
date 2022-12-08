import sqlalchemy
from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = 'lessons'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    lesson_title = sqlalchemy.Column(sqlalchemy.String)
    img_path = sqlalchemy.Column(sqlalchemy.String)