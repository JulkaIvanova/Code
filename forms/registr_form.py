from markupsafe import Markup
from .consts import CITYES

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField, PasswordField, EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, html_params,RadioInput


class CastomListWidget(ListWidget):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        for subfield in field:
            html.append(f"<div id='sex' style='display: flex;flex-direction: row; color: #ffffff; margin-left:-24px;'><span style='margin-right:7px'>{subfield()}</span>{subfield.label}</div>")
        return Markup("".join(html))
    
class CustomRadioField(RadioField):

    widget = CastomListWidget()
    option_widget = RadioInput()


class Registration(FlaskForm):
    name = StringField('Фамилия', validators=[DataRequired()])
    surname = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст')
    city = SelectField('Город', choices=CITYES)
    sex = CustomRadioField('Пол', choices=[
        ('male', 'Мужской'),
        ('female', 'Женский'),
        ('no', 'Секрет')
    ], default='male')
    email = EmailField('Email')
    password = PasswordField('Пароль')
    password_repeat = PasswordField('Повторите пароль')
    submit = SubmitField('Готово')


    