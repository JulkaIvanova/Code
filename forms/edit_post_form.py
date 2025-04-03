from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField


class EditPostForm(FlaskForm):
    caption = TextAreaField()
    submit = SubmitField('Готово')
