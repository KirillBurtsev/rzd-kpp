from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from rzd_kpp.models import User, UserDetails
# from flask_login import login_user, logout_user, current_user, login_required

class LoginForm(FlaskForm):
    username = StringField(label='Логин', validators=[DataRequired()])
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    submit= SubmitField(label='Подтвердить')

class RegisterForm(FlaskForm):
    username = StringField(label='Логин', validators=[DataRequired(), Length(min=2, max=55)])
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    firstname = StringField(label='Имя', validators=[DataRequired(), Length(min=2, max=55)])
    lastname = StringField(label='Фамилия', validators=[DataRequired(), Length(min=2, max=55)])
    family_name = StringField(label='Отчество', validators=[Length(max=55)])
    is_admin = BooleanField(label='Администратор')
    dateofbirth = DateField(label='Дата рождения', format='%Y-%m-%d', validators=[DataRequired()])
    address = StringField(label='Адрес', validators=[DataRequired(), Length(min=2, max=55)])
    submit = SubmitField(label='Подтвердить')

class PassForm(FlaskForm):
    pass_type = StringField('Pass Type', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    expire_date = DateField('Expire Date', validators=[DataRequired()])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Create Pass')