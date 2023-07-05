from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import sqlalchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, Login, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from flask import abort
from db import CreateUser, Comment, BlogPost, db
from login import login_manager, admin_only
from api import CreateApp
from mail import send_email


app = CreateApp()

year = datetime.now().year


login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(CreateUser, user_id)

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)



@app.route('/')
def get_all_posts():
    
    posts = db.session.execute(db.select(BlogPost)).scalars().all()
    return render_template("index.html", all_posts=posts, user = current_user, date =year)


@app.route('/register', methods = ["POST", "GET"])
def register():

    form =  RegisterForm()

    if form.validate_on_submit():
        user = {
            "email": form.email.data,
            "name": form.name.data,
            "password": generate_password_hash(password = form.password.data, method='pbkdf2:sha256',
            salt_length=8)

        }

        user = CreateUser(**user)
        try:
            db.session.add(user)
            db.session.commit()
            
        except sqlalchemy.exc.IntegrityError:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for("login"))
        else:
            
            db.session.refresh(user)
            login_user(user)
            
            return redirect(url_for("get_all_posts"))
    return render_template("register.html", form = form, user = current_user, date= year)


@app.route('/login', methods = ["POST", "GET"])
def login():
    form = Login()

    if form.validate_on_submit():
        user = db.session.execute(db.select(CreateUser).filter_by(email = form.email.data)).scalars().first()
        if user:
        
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                
                
                return redirect(url_for("get_all_posts"))

    return render_template("login.html", form = form, user =current_user, date = year)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def show_post(post_id):
    form = CommentForm()
    requested_post = db.session.get(BlogPost, post_id)
    comments = requested_post.comments
    if form.validate_on_submit():
        new_comment = Comment(
            text = form.comment_body.data,
            user_id = current_user.id,
            user = current_user,
            parent_post = requested_post,
            post_id = requested_post.id
        )
        db.session.add(new_comment)
        db.session.commit()
        db.session.refresh(requested_post)
        comments = requested_post.comments
    
    
    return render_template("post.html", post=requested_post, user = current_user, date= year, form = form, comments = comments)


@app.route("/about")
def about():
    return render_template("about.html", user = current_user, date = year)


@app.route("/contact", methods = ["POST", "GET"])
def contact():
    if request.method == "POST":
        sender = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]
        send_email(sender, message, phone)
        return redirect(url_for("get_all_posts"))

    return render_template("contact.html", user = current_user, date = year)


@app.route("/new-post", methods =["POST", "GET"])
@admin_only
def add_new_post():
    print(current_user.name)
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
            author_id=current_user.id,
            
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, user = current_user, date = year)


@app.route("/edit-post/<int:post_id>")
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form, user = current_user, date= year)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

# @app.route("/register")
# def register():
#     return render_template("register.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug= True)
