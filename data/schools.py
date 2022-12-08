import sqlalchemy
from .db_session import SqlAlchemyBase


class School(SqlAlchemyBase):
    __tablename__ = 'schools'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    school_title = sqlalchemy.Column(sqlalchemy.String)
    img_path = sqlalchemy.Column(sqlalchemy.String)