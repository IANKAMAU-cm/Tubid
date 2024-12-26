from wtforms import SelectField
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username', 
        validators=[DataRequired(), Length(min=3, max=20)], 
        render_kw={"class": "form-control", "placeholder": "Enter your username"}
    )
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()], 
        render_kw={"class": "form-control", "placeholder": "Enter your email"}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired(), Length(min=6)], 
        render_kw={"class": "form-control", "placeholder": "Enter your password"}
    )
    confirm_password = PasswordField(
        'Confirm Password', 
        validators=[DataRequired(), EqualTo('password')], 
        render_kw={"class": "form-control", "placeholder": "Confirm your password"}
    )
    role = SelectField(
        'Role',
        choices=[('admin', 'Admin'), ('seller', 'Seller'), ('buyer', 'Buyer')],
        validators=[DataRequired()],
        render_kw={"class": "form-select"}
    )
    submit = SubmitField('Register', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please use a different email address.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[DataRequired(), Email()], 
        render_kw={"class": "form-control", "placeholder": "Enter your email"}
    )
    password = PasswordField(
        'Password', 
        validators=[DataRequired()], 
        render_kw={"class": "form-control", "placeholder": "Enter your password"}
    )
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})