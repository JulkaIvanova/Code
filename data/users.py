import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    age = sqlalchemy.Column(sqlalchemy.Integer)
    city = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    post_ids = sqlalchemy.Column(sqlalchemy.String)
    comment_ids = sqlalchemy.Column(sqlalchemy.String)
    post_like_ids = sqlalchemy.Column(sqlalchemy.String)
    post_like_guide_category_ids = sqlalchemy.Column(sqlalchemy.String)
    post_like_ideas_category_ids = sqlalchemy.Column(sqlalchemy.String)
    post_like_mems_category_ids = sqlalchemy.Column(sqlalchemy.String)
    post_like_common_category_ids = sqlalchemy.Column(sqlalchemy.String)
    friends_ids = sqlalchemy.Column(sqlalchemy.String)
    friends_requests = sqlalchemy.Column(sqlalchemy.String)
    chats_ids = sqlalchemy.Column(sqlalchemy.String)
    img_profile = sqlalchemy.Column(sqlalchemy.String)
    img_avatar = sqlalchemy.Column(sqlalchemy.String)
    sex = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)


    comments = orm.relationship("Comments", back_populates='user')
    posts = orm.relationship("Posts", back_populates='user')
    # chats = orm.relationship("Chat", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
