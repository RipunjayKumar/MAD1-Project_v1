from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projectDB.sqlite3'
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = "users"
    userId = db.Column(db.Integer, primary_key = True, autoincrement = True)
    firstName = db.Column(db.String(32), nullable=False)
    lastName = db.Column(db.String(32))
    userName = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(50),nullable=False)
    isAdmin = db.Column(db.Boolean,default=False)

class Sections(db.Model):
    __tablename__ ="sections"
    sectionId = db.Column(db.Integer, primary_key = True, autoincrement = True)
    sectionName = db.Column(db.String(50), nullable=False, unique=True)
    dateCreated = db.Column(DateTime, default=db.func.now())
    books = db.relationship('Books', backref='sections')

class Books(db.Model):
    __tablename__ = "books"
    bookId = db.Column(db.Integer, primary_key = True, autoincrement = True)
    bookName = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.String(200), nullable=False)
    authors = db.Column(db.String(200), nullable=False)
    issuedDate = db.Column(DateTime)
    returnDate = db.Column(DateTime)
    sectionId = db.Column(db.Integer,db.ForeignKey('sections.sectionId'),nullable=False)



with app.app_context():
    db.create_all()


@app.route("/index")
def index():
    return render_template('index.html')

@app.route('/issue')
def issue():
    return render_template('issue.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)

        user = User.query.filter_by(userName = username).first()
        if user.password == password:
            return redirect(url_for('index'))
        else:
            return redirect (url_for('error'))
    return render_template('login.html')

@app.route('/addSection', methods=['GET','POST'])
def addSection():
    if request.method == "POST":
        section = Sections(
            sectionName = request.form.get('sectionName')
        )

        db.session.add(section)
        db.session.commit()

        return render_template('addSection.html')
    else:
        return render_template('addSection.html')
    return render_template('index.html')


@app.route('/addBook', methods=['GET','POST'])
def addBook():
    sections  = Sections.query.all()

    if request.method == "POST":

        book = Books(
            bookName = request.form.get('bookName'),
            content = request.form.get('content'),
            authors = request.form.get('authors'),
            sectionId = request.form.get('sectionId')
        )

        db.session.add(book)
        db.session.commit()

        return render_template('addBook.html', sections = sections)
    else:
        return render_template('addBook.html', sections = sections)

    return render_template('error.html')


@app.route('/error')
def error():
    return "Something went wrong"

if __name__ == "__main__":
    app.run(
        debug=True
    )