from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo,NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SHA512Form(FlaskForm):
    plaintext = StringField('Text Input',validators=[DataRequired()])
    submit = SubmitField('SHA512 Hash')

class KeyForm(FlaskForm):
    keysize = SelectField('Select keysize (Byte)',choices = ['16','24','32'])
    submit = SubmitField('Generate Key')

class PKIForm(FlaskForm):
    keysize = IntegerField('Key Size Bits:',
                           validators=[DataRequired(),NumberRange(min=1024, max=4096)])
    submit = SubmitField('Generate Key')

    
