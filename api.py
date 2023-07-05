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
from db import CreateUser, Comment, BlogPost, db, bs
from login import login_manager
from config import settings



def CreateApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = settings.secret
    ckeditor = CKEditor(app)
    

    ##CONNECT TO DB
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bs.init_app(app)
    
    login_manager.init_app(app)

    return app
    
