from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        from models import User
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя уже занято.')

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    body = TextAreaField('Текст заметки', validators=[DataRequired()])
    tags = StringField('Теги (через запятую)')
    submit = SubmitField('Сохранить')