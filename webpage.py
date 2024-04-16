from flask import Flask, flash, redirect, request, url_for, render_template
import os
from werkzeug.utils import secure_filename 
from dotenv import load_dotenv

load_dotenv()
UPLOAD_FODLER = 'static\images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
SECRET_KEY = os.getenv("secret_key")


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FODLER
app.config["SECRET_KEY"] = SECRET_KEY

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
    print(file)
    if file.filename == '':
      flash('No selected file')
      return redirect(request.url)
    if file and allowed_file(file.filename):
      print("WE GOT A FILE")
      filename = secure_filename(file.filename)
      file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return redirect(url_for('home',
                              filename=filename))
  



if __name__ == '__main__':
  app.run(debug =True)