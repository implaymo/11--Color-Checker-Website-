from flask import Flask, flash, redirect, request, url_for, render_template
import os
from werkzeug.utils import secure_filename 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import cv2 
import numpy as np

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


load_dotenv()
UPLOAD_FODLER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.getenv("secret_key")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FODLER
app.config["SECRET_KEY"] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db.init_app(app)

class ImageStore(db.Model):
    __tablename__ = 'image_store'
    id: Mapped[int] = mapped_column(primary_key=True)
    img_url: Mapped[str] = mapped_column(unique=True)
 


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route("/",  methods=["GET", "POST"])
def home():
  image = db.get_or_404(ImageStore, 1)
  print(image.img_url)
  check_image_colors(image=f"static/images/{image.img_url}")
  return render_template("index.html", image=image)

@app.route("/upload", methods=["GET", "POST"])
def upload():
  if request.method == "POST":
    if 'file' not in request.files:
      print("NO FILE")
      flash("No file part")
      return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      delete_image()
      filename = secure_filename(file.filename) 
      update_image(filename=filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('home',
                              filename=filename))  
      
def delete_image():
  try:
    stored_image_id = 1
    image = db.get_or_404(ImageStore, stored_image_id)
    db.session.delete(image)
    db.session.commit()
  except Exception as e:
    print(f"ERROR: {e}")
    
def update_image(filename):
  new_image = ImageStore(img_url=filename)
  db.session.add(new_image)
  db.session.commit()
  
def check_image_colors(image):
  check_image = cv2.imread(image)
  image_rgb = cv2.cvtColor(check_image, cv2.COLOR_BGR2RGB)
  
  pixel_values = image_rgb[0,0]
  
  print("Color values of the first pixel:", pixel_values)
  
  



if __name__ == '__main__':
  app.run(debug =True)