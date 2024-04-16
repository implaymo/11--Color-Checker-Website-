from flask import Flask, flash, redirect, request, url_for, render_template
import os
from werkzeug.utils import secure_filename 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


load_dotenv()
UPLOAD_FODLER = 'static\images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.getenv("secret_key")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FODLER
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class ImageStore(db.Model):
    __tablename__ = 'image_store'
    id = db.Column(db.Integer, primary_key=True) 
    img_url = db.Column(db.String, unique=True)

with app.app_context():
    db.create_all()