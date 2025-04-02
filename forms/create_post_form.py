from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, RadioField, PasswordField, EmailField, FileField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets import ListWidget, html_params,RadioInput
from flask_wtf.file import FileSize, FileAllowed, MultipleFileField

class CastomListWidget(ListWidget):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = []
        for subfield in field:
            html.append(f"<div id='category'>{subfield()}<span class='radio-label'>{subfield.label}</span></div>")
        return Markup("".join(html))
    
class CustomRadioField(RadioField):

    widget = CastomListWidget()
    option_widget = RadioInput()


class CreatePostForm(FlaskForm):
    imgs = MultipleFileField(validators=[
        FileAllowed(['jpg', 'jpeg', 'png']),
        FileSize(max_size=10 * 1024 * 1024)
    ])
    caption = TextAreaField()
    category = CustomRadioField(choices=[
        ('common', '#Общее'),
        ('guide', '#Гайды'),
        ('mems', '#Мемы'),
        ('ideas', '#Идеи')
    ], default='common')
    submit = SubmitField('Готово')
