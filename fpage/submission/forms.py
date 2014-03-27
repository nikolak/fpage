from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired, Length, URL


class SubmitForm(Form):
    url = TextField('URL', validators=[URL(), DataRequired(), Length(min=3, max=140)])
    title = TextField('Title', validators=[DataRequired(), Length(min=3, max=399)])