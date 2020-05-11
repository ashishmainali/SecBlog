from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm, SHA512Form, KeyForm,PKIForm
from security import generate_secret_key_for_AES_cipher,generate_public_private_key
import hashlib
app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)



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
    if form.validate_on_submit():
            flash('Key Generation successful', 'success')
            return render_template('PKI.html', title='Generate Public Private Keys', form=form,key=generate_public_private_key(int(form.keysize.data)) )
    return render_template('generatekey.html', title='Generate AES Key', form=form)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
