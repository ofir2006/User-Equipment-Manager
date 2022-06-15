from hashlib import sha256
import re
from flask import Blueprint, redirect, render_template, request, flash
from .models import User, Admin, Item
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import current_user, login_user, login_required, logout_user


auth = Blueprint('auth', __name__)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        email = request.form.get('email')
        password = request.form.get('password')
        passwordConfirm = request.form.get('passwordConfirm')

        user = Admin.query.filter_by(email=email).first()

        if user:
            flash("Email is already being used!",category="error")
        elif len(firstName) < 2:
            flash("Name cannot be less than 2 characters long",category="error")
        elif len(lastName) < 2:  
            flash("Last name cannot be less than 2 characters",category="error")
        elif len(email) < 4:
             flash("Invalid email!", category="error")
        elif password != passwordConfirm:
             flash("passwords do not match!", category="error")
        elif len(password) < 7:
            flash("Password must be at least 7 characters long", category="error")
        else:
            new_user = Admin(firstName=firstName,lastName=lastName,password=generate_password_hash(password, method='sha256'), email=email)
            db.session.add(new_user)
            db.session.commit()
            flash("Registered successfully!", category="success")
            return redirect('/')


    return render_template("sign-up.html")

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Admin.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect("/")
        else:
            flash("Log in failed, please check your username and password.", category="error")
        
    return render_template("login.html")

@auth.route('/logout')
@login_required
def log_out():
    logout_user()
    return redirect('/')


@auth.route('/change-password', methods=['GET','POST'])
def changepassword():
    user = ''
    if request.method == 'POST':
        currentPassword = current_user.password
        oldpw = request.form.get('oldpassword')
        newPassword = request.form.get('newpassword')
        confirmPassword = request.form.get('confirmpassword')
        newPasswordHash = generate_password_hash(newPassword,'sha256')

        if not check_password_hash(currentPassword, oldpw):
            flash("Password is incorrect!")

        elif newPassword != confirmPassword:
            flash('Passwords do not match!', category="error")

        else:
            flash('Password changed successfully!', category='success')
            current_user.password = newPasswordHash
            db.session.commit()


    return render_template('change-password.html', user=current_user, page='changePassword')