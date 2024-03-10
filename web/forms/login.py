from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from sqlalchemy_serializer import SerializerMixin


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('запомнить меня')
    submit = SubmitField('Войти')