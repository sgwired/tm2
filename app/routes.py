from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.forms import EditProfileForm
from app.models import User
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
    # user = {'username': 'Shelton'}
    toys = [
        {
            'maker': {'username': 'John'},
            'name': 'The Frisbee!'
        },
        {
            'maker': {'username': 'Susan'},
            'name': 'The Avengers Action Figure!'
        }
    ]
    return render_template('index.html', title='Home', toys=toys)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    toys = [
        {'maker': user, 'name': 'Big Wheel'},
        {'maker': user, 'name': 'Barbie Dream House'},
        {'maker': user, 'name': 'Super Soaker'}
    ]
    return render_template('user.html', user=user, toys=toys)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.address1 = form.address1.data
        current_user.address2 = form.address2.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.postal_code = form.postal_code.data
        current_user.phone = form.phone.data
        current_user.website = form.website.data
        current_user.facebook = form.facebook
        current_user.twitter = form.twitter.data
        current_user.instagram = form.instagram.data
        current_user.company = form.company.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.address1.data = current_user.address1
        form.address2.data = current_user.address2
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.postal_code.data = current_user.postal_code
        form.phone.data = current_user.phone
        form.website.data = current_user.website
        form.facebook.data = current_user.facebook
        form.twitter.data = current_user.twitter
        form.instagram.data = current_user.instagram
        form.company.data = current_user.company
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)