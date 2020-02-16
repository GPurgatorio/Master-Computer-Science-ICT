import wtforms as f
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email


class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired(), Email()])
    firstname = f.StringField('firstname', validators=[DataRequired()])
    lastname = f.StringField('lastname', validators=[DataRequired()])
    password = f.PasswordField('password', validators=[DataRequired()])
    dateofbirth = f.DateField('dateofbirth', format='%d/%m/%Y')
    display = ['email', 'firstname', 'lastname', 'password', 'dateofbirth']


class StoryForm(FlaskForm):
    text = f.TextAreaField('text',
                           validators=[DataRequired(),
                                       Length(min=1, max=1000, message='Your story is too long (max 1000 characters)')])
    as_draft = f.HiddenField('is_draft')
    display = ['text']
    hidden = ['is_draft']
