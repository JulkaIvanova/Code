import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class PrivateChat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "private_chats"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    messeges = sqlalchemy.Column(sqlalchemy.String)
    members = sqlalchemy.Column(sqlalchemy.String)
    chat_name = sqlalchemy.Column(sqlalchemy.String)
    chat_avatar = sqlalchemy.Column(sqlalchemy.String)
    comments = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
