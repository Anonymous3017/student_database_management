'''
 ToDo app with authentication in Flask framework. I have to use Flask and SQLAlchemy extensions to handle user sessions and database operations. I have to also add some basic validations and error handling. The app should has the following endpoints:

/api/todo/register: To register a new user with username and password
/api/todo/login: To log in an existing user with username and password
/api/todo/logout: To log out the current user
/api/todo: To get all the todo items for the current user
/api/todo/<int:id>: To get, update or delete a specific todo item for the current user
The app uses a SQLite database to store the user and todo data. You can change it to any other database by modifying the SQLALCHEMY_DATABASE_URI configuration.'''

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

#Define the users table model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

#Route for the user registration
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            # Create a new user object
            user = User(username=request.form['username'], password=request.form['password'])

            with app.app_context():
                # Add the user to the database
                db.session.add(user)
                db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('login'))

    # Render the registration form
    return render_template('signup.html')


#Route for the user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            flash('Please enter all the fields', 'error')
        else:
            # Get the user from the database
            user = User.query.filter_by(username=request.form['username']).first()
            if user and user.password == request.form['password']:
                flash('Login successful')
                return redirect(url_for('show_all'))
            else:
                flash('Login failed', 'error')

    # Render the login form
    return render_template('login.html')

#Route for the user logout
@app.route('/logout')
def logout():
    flash('Logout successful')
    return redirect(url_for('login'))

# Define the students table model
class Students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, city, addr, pin):
        self.name = name
        self.city = city
        self.addr = addr
        self.pin = pin

# Route for the home page, displays all students
@app.route('/')
def show_all():
    with app.app_context():
        return render_template('show_all.html', students=Students.query.all())

# Route for adding a new student
@app.route('/new', methods=['GET', 'POST'])
def new():
    # Handle form submission
    if request.method == 'POST':
        # Validate form input
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            # Create a new student object
            student = Students(request.form['name'], request.form['city'], request.form['addr'], request.form['pin'])

            with app.app_context():
                # Add the student to the database
                db.session.add(student)
                db.session.commit()

            flash('Record was successfully added')
            return redirect(url_for('show_all'))

    # Render the new student form
    return render_template('new.html')


# Route for editing a student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Get the student from the database
    student = Students.query.get(id)

    # Handle form submission
    if request.method == 'POST':
        # Validate form input
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            form_id = request.form['id']
            name = request.form['name']
            city = request.form['city']
            addr = request.form['addr']
            pin = request.form['pin']
            # print(f"Received form data: id={form_id}, name={name}, city={city}, addr={addr}, pin={pin}")
            # Update the student object
            student.name = name
            student.city = city
            student.addr = addr
            student.pin = pin

            with app.app_context():
                # Update the student in the database
                db.session.commit()
                print(f"Updated student record: id={form_id}, name={name}, city={city}, addr={addr}, pin={pin}")
                # Check if the transaction was committed
                if not db.session.is_active:
                    print("\n Transaction was not committed")


            flash('Record was successfully updated')
            return redirect(url_for('show_all'))

    # Render the edit student form
    return render_template('edit.html', student=student)

# route for delete a student
@app.route('/delete', methods=['POST'])
def delete():
    student_id = request.form['id']
    student = Students.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Record was successfully deleted')
    else:
        flash('Student record not found', 'error')
    return redirect(url_for('show_all'))

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables if they don't exist
        db.create_all()
        

    # Start the Flask application
    app.run(debug=True)

#     ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#     from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'secret_key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)

# # Define the User model
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(120), nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

# # Define the login route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             login_user(user)
#             flash('Login successful')
#             return redirect(url_for('show_all'))