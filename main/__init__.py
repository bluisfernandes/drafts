from flask import Flask
from markupsafe import escape
from flask import url_for
from flask import render_template
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>Hello, World!</p>"
    

@app.route("/<name>")
def hello2(name):
    return f"Hello, {escape(name)}!"


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/projects/')
def projects():
    return 'The project page'


@app.route('/about')
def about():
    return 'The about page'


@app.route('/variables/')
def variables():
    var = list(os.environ.keys())
    return str(var)




@app.route('/index')
def index():
    return 'index'

# @app.route('/login')
# def login():
#     return 'login'

@app.route('/users/<username>')
def profile(username):
    return f'{username}\'s profile'


from flask import request

def do_the_login():
    return "do the login"
def show_the_login_form():
    return "show_the_login_form"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return do_the_login()
    else:
        return show_the_login_form()


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)



with app.test_request_context():
    print(url_for('index'))
    print(url_for('home'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('hello', name='robert'))
    url_for('static', filename='style.css')


# Cookies

from flask import make_response

@app.route('/cookie/<name>')
def set_cookie(name):
    resp = make_response(render_template('hello.html', name='set cookie'))
    resp.set_cookie('username', name)
    return resp

@app.route('/cookie/')
def read_cookie():
    resp = request.cookies.get('username')
    return render_template('hello.html', name=resp)




from flask import abort, redirect, url_for

@app.route('/redirect/')
def redir():
    return redirect(url_for('index'))

@app.route('/logina')
def logina():
    abort(401)


@app.route('/dict')
def dictionary():
    dic= {'name': "Bruno", "age":30, "location":{"lat":-20, "long":46}}
    return dic



from flask import session, flash
import secrets

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = secrets.token_hex()
# app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/indexb')
def indexb():
    if 'username' in session:
        return f'Logged in as {session["username"]}'
    return 'You are not logged in'

@app.route('/loginb', methods=['GET', 'POST'])
def loginb():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('indexb'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('You were successfully logged out')
    return redirect(url_for('indexb'))

@app.route("/session/")
def print_session():
    app.logger.debug('A value for debugging')
    print(session)
    return str(session)

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')