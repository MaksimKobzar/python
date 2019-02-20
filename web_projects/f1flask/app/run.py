from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '80dda5ffe04140226b924eff4ab042b4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    """docstring for User"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    """docstring for Post"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}', '{self.content}')"


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


if __name__ == '__main__':
    app.run(debug=True)
