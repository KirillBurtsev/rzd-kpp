from rzd_kpp import app, db, bcrypt
from flask import render_template, url_for, request, redirect, flash, abort, session
from rzd_kpp.forms import LoginForm, RegisterForm, PassForm, PassTypeForm
from rzd_kpp.models import User, UserDetails, Pass, PassType, UserPass
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
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            Login=form.username.data,
            Password=hashed_password
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

@app.route('/admin/create-pass', methods=['GET', 'POST'])
def admin_create_pass():
    form = PassForm()
    users = User.query.all()  # Fetch all users for the dropdown
    pass_types = PassType.query.all()  # Fetch all pass types for the dropdown

    if request.method == 'POST':
        user_id = request.form.get('user_id')  # Get selected user ID
        pass_type_id = request.form.get('pass_type_id')  # Get selected pass type ID
        start_date = form.start_date.data
        expire_date = form.expire_date.data
        is_active = form.is_active.data

        if user_id and pass_type_id:
            try:
                # Create the Pass instance
                new_pass = Pass(
                    PassTypeID=pass_type_id,
                    StartDate=start_date,
                    ExpireDate=expire_date,
                    IsActive=is_active
                )
                db.session.add(new_pass)
                db.session.commit()

                # Link the pass to the selected user
                user_pass = UserPass(
                    UserID=int(user_id),
                    PassID=new_pass.PassID
                )
                db.session.add(user_pass)
                db.session.commit()

                flash('Pass created and assigned successfully!', 'success')
                return redirect(url_for('admin'))
            except Exception as e:
                db.session.rollback()
                flash(f'An error occurred: {e}', 'danger')
        else:
            flash('Please select a user and pass type.', 'danger')

    return render_template(
        'create_pass.html',
        form=form,
        users=users,
        pass_types=pass_types
    )

@app.route('/admin/create-type', methods=['GET', 'POST'])
def admin_create_type():
    form = PassTypeForm()  # Assume you have a WTForm for creating a PassType
    if form.validate_on_submit():
        new_pass_type = PassType(
            Name=form.name.data
        )
        try:
            db.session.add(new_pass_type)
            db.session.commit()
            flash('Новый тип пропуска успешно создан!', 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()
            print(f"Error occurred: {e}")
            flash('Ошибка при создании типа пропуска. Попробуйте снова.', 'danger')
    return render_template('create_type.html', form=form)