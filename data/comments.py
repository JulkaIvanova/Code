import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Comments(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "comments"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    chat_id = sqlalchemy.Column(
        sqlalchemy.Integer
    )
    text = sqlalchemy.Column(sqlalchemy.String)
    send_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    sender = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    # post = orm.relationship("Posts")
    user = orm.relationship("User")



