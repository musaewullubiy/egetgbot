import sqlalchemy
from .db_session import SqlAlchemyBase


class Payment(SqlAlchemyBase):
    __tablename__ = 'payments'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    channel_id = sqlalchemy.Column(sqlalchemy.String)
    user_id = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer)
