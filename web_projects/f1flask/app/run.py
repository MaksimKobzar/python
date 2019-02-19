from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '80dda5ffe04140226b924eff4ab042b4'

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
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='It`s about page.')


@app.route('/register')
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
