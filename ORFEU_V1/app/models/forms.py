from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    nome_usuario = StringField('nome_usuario', validators=[DataRequired()])
    senha_usuario = PasswordField('senha_usuario', validators=[DataRequired()])
    lembrar_me = BooleanField('lembrar_me')
