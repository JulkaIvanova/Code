from flask_wtf import FlaskForm
from wtforms import StringField


class SerchUserForm(FlaskForm):
    serch_user_id = StringField()