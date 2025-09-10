from flask import Flask, render_template, redirect, url_for, flash, request
from forms import LoginForm, RegisterForm
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

DB_FILE = 'database.db'

# Initialize database
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                email TEXT UNIQUE,
                dob TEXT,
                phone TEXT,
                password TEXT
            )
        ''')
        conn.commit()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username_or_email = form.username_or_email.data
        password = form.password.data

        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE (username = ? OR email = ?) AND password = ?",
                  (username_or_email, username_or_email, password))
        user = c.fetchone()
        conn.close()

        if user:
            flash('✅ Login successful', 'success')
            return redirect(url_for('login'))  # Redirect to homepage/dashboard later
        else:
            flash('❌ Login denied: Invalid username/email or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm_password.data:
            flash('❌ Passwords do not match!', 'danger')
            return render_template('register.html', form=form)

        username = form.username.data
        email = form.email.data
        dob = form.dob.data
        phone = form.phone.data
        password = form.password.data

        try:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO users (username, email, dob, phone, password) VALUES (?, ?, ?, ?, ?)",
                      (username, email, dob, phone, password))
            conn.commit()
            conn.close()
            flash('✅ Registration successful!', 'success')
            # Redirect to success page instead of login
            return redirect(url_for('register_success'))
        except sqlite3.IntegrityError:
            flash('❌ Username or Email already exists!', 'danger')
    return render_template('register.html', form=form)

# New route for registration success page
@app.route('/register_success')
def register_success():
    return render_template('register_success.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
