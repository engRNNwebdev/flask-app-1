from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
from wtforms import Form, BooleanField, StringField, PasswordField, validators

class SubmitMOS(Form):
    mosObject = StringField('Username', [validators.Length(min=4, max=25)])
    slug = StringField('Email Address', [validators.Length(min=6, max=35)])
    description = StringField('Email Address', [validators.Length(min=6, max=35)])
    confirm = StringField('Email Address', [validators.Length(min=6, max=35)])
    localFile = BooleanField('I accept the TOS', [validators.DataRequired()])
