import datetime
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Posts(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "posts"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    likes = sqlalchemy.Column(
        sqlalchemy.Integer
    )
    caption = sqlalchemy.Column(sqlalchemy.String)
    comments_ids = sqlalchemy.Column(sqlalchemy.String)
    create_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    imgs = sqlalchemy.Column(sqlalchemy.String)
    category = sqlalchemy.Column(sqlalchemy.String)
    creater = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")
    )
    isWithPyCode = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    code = sqlalchemy.Column(sqlalchemy.String)
    likes_user_id = sqlalchemy.Column(sqlalchemy.String)
    user = orm.relationship("User")
