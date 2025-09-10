from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo, ValidationError

def phone_number_check(form, field):
    if not field.data.startswith('+234') or len(field.data) != 14:
        raise ValidationError('Phone number must start with +234 and be followed by 10 digits.')

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=20),
        Regexp('^[A-Za-z0-9]+$', message='Username must be alphanumeric')
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), phone_number_check])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6),
        Regexp('^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*?&])',
               message='Password must be alphanumeric and include a special character')
    ])
    confirm_password = PasswordField('Retype Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')
