# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL


class RegisterForm(Form):
    username = TextField('Username', validators=[DataRequired(), Length(min=3, max=25)])
    email = TextField('Email', validators=[Optional(), Email(), Length(min=0, max=40)])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(
        'Verify password',
        [DataRequired(), EqualTo('password', message='Passwords must match')])


class LoginForm(Form):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])


class SubmitForm(Form):
    url = TextField('URL', validators=[URL(), DataRequired(), Length(min=3, max=140)])
    title = TextField('Title', validators=[DataRequired(), Length(min=3, max=399)])


class CommentForm(Form):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=5000)])