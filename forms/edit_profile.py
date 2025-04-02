from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, IntegerField, SubmitField, FileField
from wtforms import BooleanField
from wtforms.validators import DataRequired


class SettingsForm(FlaskForm):
    client_id = StringField('ID', render_kw={'readonly': True})
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    avatar = FileField('Выбирите фото профиля')
    background = FileField('Выбирите фон профиля')
    submit = SubmitField('Сохранить настройки')