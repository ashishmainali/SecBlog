from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SHA512Form, KeyForm,PKIForm
from security import generate_secret_key_for_AES_cipher,generate_public_private_key
import hashlib
from flask import request, redirect
from werkzeug.utils import secure_filename
from stegano import lsb

import os
from flask.helpers import send_file

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

app.config["IMAGE_UPLOADS"] = os.getcwd() + '/uploads/'
app.config["IMAGE_UPLOADS_REAVEAL"] = os.getcwd() + '/reveal/'
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


posts = [
    {
        'author': 'Ashish Mainali',
        'title': 'Added Private Key Generation Modulde',
        'content': 'Added private key generatation modulde to the website today.',
        'date_posted': 'April 30, 2020'
    },
    {
        'author': 'Anon',
        'title': 'Testing',
        'content': 'Tested the private key generation module and it is working well.',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/SHA512", methods=['GET', 'POST'])
def SHA512():
    form = SHA512Form()
    if form.validate_on_submit():
        if form.plaintext.data.strip():
            flash('Hashing Complete', 'success')
            return render_template('SHA512.html', title='SHA512', form=form,hash= hashlib.sha512(form.plaintext.data.encode()).hexdigest())
        else:
            flash('The input cannot be empty. Please try again!', 'danger')
    return render_template('SHA512.html', title='SHA512', form=form)

@app.route("/generatekeys", methods=['GET', 'POST'])
def keygen():
    form = KeyForm()
    if form.validate_on_submit():
            flash('Key Generation Complete', 'success')
            return render_template('generatekey.html', title='Generate AES Keys', form=form,key= generate_secret_key_for_AES_cipher(int(form.keysize.data)))
    return render_template('generatekey.html', title='Generate AES Key', form=form)

@app.route("/pki", methods=['GET', 'POST'])
def PKI():
    form = PKIForm()
    if request.method == 'POST':
        if form.validate_on_submit():
                flash('Key Generation successful', 'success')
                return render_template('PKI.html', title='Generate Public Private Keys', form=form, key=generate_public_private_key(int(form.keysize.data)))
        else:
            flash('Invalid Key size! Select a key size between 1024 to 4096','danger')
    return render_template('generatekey.html', title='Generate AES Key', form=form)


@app.route("/hide", methods=["GET", "POST"])
def upload_image():
    form = SHA512Form()
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    flash("Filesize exceeded maximum limit",'danger')
                    return redirect(request.url)
                image = request.files["image"]
                
                if image.filename == "":
                    flash("No file selected",'danger')
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
                    secret = lsb.hide(app.config["IMAGE_UPLOADS"] + filename, form.plaintext.data.encode("utf-8"))
                    secret.save(os.path.join(app.config["IMAGE_UPLOADS"], 'secret-' + filename))
                    return send_file(app.config["IMAGE_UPLOADS"] + 'secret-' + filename, as_attachment=True)
                    flash('Hiding message successful','success')
                    return redirect(request.url)

                else:
                    flash("That file extension is not allowed",'danger')
                    return redirect(request.url)

    return render_template("upload_new.html",title = "Stegano", form= form)

@app.route("/reveal", methods=["GET", "POST"])
def reveal_image():
    form = SHA512Form()
    if request.method == "POST":
        if request.files:
            if "filesize" in request.cookies:
                if not allowed_image_filesize(request.cookies["filesize"]):
                    flash("Filesize exceeded maximum limit",'danger')
                    return redirect(request.url)
                image = request.files["image"]
                
                if image.filename == "":
                    flash("No filename",'danger')
                    return redirect(request.url)

                if allowed_image(image.filename):
                    filename = secure_filename(image.filename)
                    image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'secret\\' +filename))
                    clear_message = lsb.reveal(app.config["IMAGE_UPLOADS"] + 'secret\\' + filename)
                    if clear_message != None:
                        return render_template("reveal.html", title="Revel Secret Text", message=clear_message)
                    else:
                        flash('No Secret Messages in this file', 'danger')
                        return redirect(request.url)

                else:
                    flash("That file extension is not allowed",'danger')
                    return redirect(request.url)

    return render_template("reveal.html",title = "Stegano")






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
