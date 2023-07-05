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
from db import CreateUser, Comment, BlogPost



login_manager = LoginManager()

def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwags):
        
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwags)
    return wrapper