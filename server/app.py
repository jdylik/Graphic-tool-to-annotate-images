from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '9332b72257e534031beb9c8ab9674c23'
CORS(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/name')
def name():  # put application's code here
    return json.dumps({"name": "Tutaj będzie można dodać adnotacje do zdjęć."}, ensure_ascii=False)

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


if __name__ == '__main__':
    app.run(debug=True)