from flask import render_template, url_for, flash, redirect
from app import app
from app.forms import RegistrationForm, LoginForm
from app.models import User, Post


posts = [
    {
        'author': 'Maksim Kobzar',
        'title': 'Blog Post 1',
        'content': 'My first post content',
        'date_posted': 'Febrary 19, 2019'
    },
    {
        'author': 'Alex Pushkin',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Febrary 12, 1712'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='F1Flask', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='ABOUT')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    print('After RegistrationForm')
    if form.validate_on_submit():
        print('Redirect is coming!')
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    else:
        print('Not validate!')
        return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash(f'Successfull login! Glad to see you, {form.username.data}.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Unsuccessfull login! Please try another logina and password.', 'danger')
    return render_template('login.html', title='Login', form=form)