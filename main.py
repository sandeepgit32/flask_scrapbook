from flask import render_template, request, redirect, url_for, session
from datetime import datetime
from models import User, Blogpost
from flask_bcrypt import Bcrypt
from functools import wraps
from app import app
from db import db


bcrypt_obj = Bcrypt(app)


def authentication_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs): 
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            return render_template('login.html')
    return wrapper


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Hashing the password
        hashPassword = bcrypt_obj.generate_password_hash(request.form['password'])
        try:
            user_obj = User(
                username = request.form['username'], 
                password = hashPassword
            )
            db.session.add(user_obj)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('index.html', message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        u = request.form['username']
        p = request.form['password']  # Hashing the password
        data = User.query.filter_by(username=u).first()
        if data is not None:
            # Password is checked
            if bcrypt_obj.check_password_hash(data.password, p): 
                session['logged_in'] = True
                session['user'] = u # Store the username in session variable for display after redirection
                return redirect(url_for('index'))
        return render_template('login.html', message="Incorrect Details")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    session['user'] = None
    return redirect(url_for('index'))


@app.route('/')
@authentication_required
def index():
    posts = Blogpost.query.filter_by(author=session.get('user')).order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts, user=session.get('user'))
    

@app.route('/post/<int:post_id>')
@authentication_required
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post, user=session.get('user'))


@app.route('/add', methods=['GET', 'POST'])
@authentication_required
def add():
    if request.method == 'GET':
        return render_template('add.html', user=session.get('user'))
    else:
        post = Blogpost(
            title=request.form['title'], 
            subtitle=request.form['subtitle'], 
            author=session.get('user'), 
            content=request.form['content'], 
            date_posted=datetime.now()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/delete', methods=['GET','POST'])
@authentication_required
def delete():
    if request.method == 'GET':
        posts = Blogpost.query.filter_by(author=session.get('user')).order_by(Blogpost.date_posted.desc()).all()
        return render_template('delete.html', posts=posts, user=session.get('user'))
    else:
        post_id = request.form.get("post_id")
        post = Blogpost.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run()