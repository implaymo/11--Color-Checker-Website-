from flask import Flask, flash, redirect, request, url_for, render_template
import os
from werkzeug.utils import secure_filename 
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

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
  return render_template("index.html")

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
      try:
        stored_image_id = 1
        image = db.get_or_404(ImageStore, stored_image_id)
        db.session.delete(image)
        db.session.commit()
      except Exception as e:
        print(f"ERROR: {e}")
            
      filename = secure_filename(file.filename) 
      new_image = ImageStore(img_url=filename)
      db.session.add(new_image)
      db.session.commit()
      
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('home',
                              filename=filename))  
  



if __name__ == '__main__':
  app.run(debug =True)