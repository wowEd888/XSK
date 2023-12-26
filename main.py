from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

users = {}  # 替换为实际数据库操作
teachers = [{'id': 1, 'name': 'Professor Zhang', 'ratings': []}]

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    @staticmethod
    def get(user_id):
        return users.get(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired(), validators.Length(min=4, max=15)])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=8, max=80)])
    confirm = PasswordField('Repeat Password', validators=[validators.InputRequired(), validators.EqualTo('password')])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        users[form.username.data] = {'password': hashed_password}
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user and bcrypt.check_password_hash(users[user.id]['password'], form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html', teachers=teachers)

@app.route('/teacher/<int:teacher_id>', methods=['GET', 'POST'])
@login_required
def teacher(teacher_id):
    teacher = next((t for t in teachers if t['id'] == teacher_id), None)
    if not teacher:
        return "Teacher not found", 404
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        teacher['ratings'].append({'rating': rating, 'comment': comment, 'user': current_user.id})
    return render_template('teacher.html', teacher=teacher)

if __name__ == '__main__':
    app.run(debug=True)
