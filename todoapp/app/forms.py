from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,DateField
from wtforms.validators import DataRequired,EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password1 = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class TaskForm(FlaskForm):
	taskname=StringField('Task',validators=[DataRequired()])
	due_date=DateField('Due Date')
	submit=SubmitField('Submit')