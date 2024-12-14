from rzd_kpp import app, db
from flask import render_template, url_for, request, redirect, flash, abort, session
from rzd_kpp.forms import LoginForm, RegisterForm, PassForm
from rzd_kpp.models import User, UserDetails, Pass
# from flask_login import logout_user, current_user, login_required
from functools import wraps
from datetime import datetime
from sqlalchemy import func, text
import time


@app.route("/")
@app.route("/home")
def index():
    return render_template("homepage.html", title='Домашнаяя страница')

@app.route("/account")
def account():
    return render_template("account.html", title='Аккаунт')

@app.route("/admin")
def admin():
    return render_template("admin.html", title='Администрирование')

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(Login=form.username.data).first()
        if user and user.Password==form.password.data:
            flash(f'Успешная авторизация для пльзователя {form.username.data}')
            return redirect(url_for('index'))
        else:
            flash(f'Ошибка авторизации для пльзователя {form.username.data}', 'error')
            print(f'login:{user} and pass:{user.Password} is not match {form.password}!')
            form.username.data = ''
            form.password.data = ''
    return render_template("login.html", title='Вход', form=form)

@app.route("/logout")
def logout():
    session.pop('username', None)  # Remove the username from the session
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('index'))  # Redirect to the homepage after logout


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        user = User(
            Login=form.username.data,
            Password=form.password.data
            )
        user_details = UserDetails(
            Firstname=form.firstname.data,
            Lastname=form.lastname.data,
            Familyname=form.family_name.data,
            IsAdmin=form.is_admin.data,
            DateOfBirth=form.dateofbirth.data,
            Address=form.address.data,
            parent=user
        )
        try:
            existing_user = User.query.filter_by(Login=user.Login).first()
            if existing_user:
                flash('Пользователь с таким логином уже существует.', 'danger')
                return redirect(url_for('register'))
            db.session.add(user)
            db.session.add(user_details)
            db.session.commit()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            flash('Ошибка при регистрации. Попробуйте еще раз.', 'danger')
    else:
        print("Form validation failed")
        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
    return render_template('register.html', title='Регистрация', form=form)

@app.route('/create_pass', methods=['GET', 'POST'])
def create_pass():
    form = PassForm()
    if form.validate_on_submit():
        new_pass = Pass(
            PassType=form.pass_type.data,
            StartDate=form.start_date.data,
            ExpireDate=form.expire_date.data,
            IsActive=form.is_active.data
        )
        db.session.add(new_pass)
        db.session.commit()
        flash('New pass created successfully!', 'success')
        return redirect(url_for('admin'))  # Redirect to the admin page or pass list page

    return render_template('create_pass.html', form=form)
