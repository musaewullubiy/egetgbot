import sqlalchemy
from .db_session import SqlAlchemyBase


class Channel(SqlAlchemyBase):
    __tablename__ = 'channels'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    channel_id = sqlalchemy.Column(sqlalchemy.String)
    school_title = sqlalchemy.Column(sqlalchemy.String)
    month_title = sqlalchemy.Column(sqlalchemy.String)
    lesson_title = sqlalchemy.Column(sqlalchemy.String)
    schedule_img_path = sqlalchemy.Column(sqlalchemy.String)
