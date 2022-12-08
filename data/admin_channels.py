import sqlalchemy
from .db_session import SqlAlchemyBase


class AdminChannel(SqlAlchemyBase):
    __tablename__ = 'admin_channels'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    channel_id = sqlalchemy.Column(sqlalchemy.String)
    channel_title = sqlalchemy.Column(sqlalchemy.String)
