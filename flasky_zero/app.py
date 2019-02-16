from flask import Flask, render_template
import cgi
import os
import jinja2
from jinja2 import Environment, PackageLoader, select_autoescape

template_dir = os.path.join(os.path.dirname(__file__), 'template')
print('template_dir:' + template_dir)
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

app = Flask(__name__)
# It doesn`t work while FLASK DEBUG is set in configuration
# app.config['DEBUG'] = False

@app.route('/')
def starting_page():
    return 'It`s starting page!'

@app.route('/hello_j')
def hello_j():
    template = jinja_env.get_template('hello.html')
    return template.render()

@app.route('/hello_f')
def hello_f():
    return render_template('hello.html')

@app.route('/a')
def a():
    return render_template('a.html')

if __name__ == '__main__':
    app.run()
