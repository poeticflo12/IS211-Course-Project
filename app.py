import json
import re

from flask import Flask, render_template, request, flash, redirect,url_for
from flask_login import LoginManager,current_user, login_user, login_required,logout_user
from datetime import datetime, date , timedelta
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from models.Category import Category
from models.Post import Post
from models.momentjs import momentjs

import os
from flask_migrate import Migrate
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'f3cfe9ed8fae309f02079dbf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.jinja_env.globals['momentjs'] = momentjs

login = LoginManager(app)
login.login_view = 'login'

# from models.Test import Test

db = SQLAlchemy(app)
from models import User
migrate = Migrate(app, db)
db.init_app(app)
db.create_all()

@login.user_loader
def load_user(id):
    return User.User.query.get(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']

        user = User.User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, False)
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
 
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        email=request.form['email1']

        user = User.User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Well done! You have been registered!')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/')
def index():
    posts=Post().view_all_post()
    # return json.dumps(posts)
    return render_template("index.html",posts=posts)

@app.route("/dashboard")
@login_required
def dashboard():
    posts=Post().view_by_author(current_user.id)
    return render_template("dashboard.html",posts=posts)

@app.route("/category",methods=['GET', 'POST'])
@login_required
def category():
    if request.method=="POST":
       category_name=request.form['category_name']
       add_category=Category([category_name]).create_category()

       return redirect(url_for('index'))
    return render_template('category.html')

@app.route("/posts",methods=['GET', 'POST'])
@login_required
def posts():
    today_date=date.today()
    now_time=datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    if request.method=="POST":
        author=current_user.id
        title=request.form['title']
        content=request.form['content']
        publish_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        permalink=title.replace(' ', '-').lower() + "-" + now_time
        isPublish=1
        category_id=request.form['category']
        add_post=Post([author,title,content,publish_date,permalink,isPublish,category_id]).create_post()

        return redirect(url_for('dashboard'))
    category=Category().view_all_category()
    return render_template("new_post.html",category=category)

@app.route("/category/<id>/posts")
@login_required
def category_posts(id):
    posts=Post().view_by_category(id)
    # return json.dumps(post)
    category=Category().view_single_category(id)
    return render_template('category_posts.html',posts=posts,category=category)

@app.route("/posts/<id>/unpublish")
@login_required
def unpublish(id):
    update_post=Post().unpublish(id)
    # return id
    return redirect(url_for('dashboard'))

@app.route("/posts/<id>/publish")
@login_required
def publish(id):
    update_post=Post().publish(id)
    # return id
    return redirect(url_for('dashboard'))

@app.route("/posts/<id>/delete")
@login_required
def delete(id):
    update_post=Post().delete_post(id)
    # return id
    return redirect(url_for('dashboard'))

@app.route("/posts/<id>/edit",methods=['GET', 'POST'])
@login_required
def edit_post(id):
    today_date=date.today()
    if request.method=="POST":
        title=request.form['title']
        content=request.form['content']
        category_id=request.form['category']
        
        add_post=Post().update_post([title, content, category_id],current_user.id)

        return redirect(url_for('dashboard'))
    post=Post().view_single_post(id)

    category=Category().view_all_category()
    return render_template('edit_post.html', post=post, category=category)

@app.route("/posts/<permalink>")
@login_required
def show_post(permalink):
    post=Post().view_by_permalink(str(permalink))

    # return json.dumps(post)
    return render_template('single_post.html',post=post)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
if __name__ == "__main__":
    app.run(debug=True)