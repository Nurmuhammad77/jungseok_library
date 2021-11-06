from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'aidflh2983gf9qsbkd1ugofu1u9f'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    code = db.Column(db.String(250), unique=True, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    holder = db.Column(db.String(100), nullable=True)
    # book_owner = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    books = Book.query.all()

    if request.method == "POST":
        if request.form['select'] == 'name':
            sortedByName = Book.query.order_by(desc(Book.name)).all()

            return render_template("index.html", books=sortedByName[::-1])
        if request.form['select'] == 'code':
            sortedByCode = Book.query.order_by(desc(Book.code)).all()

            return render_template("index.html", books=sortedByCode[::-1])
    return render_template("index.html", books=books)


@app.route('/add',  methods=["POST", "GET"])
def add_book():
    if request.method == "POST":

        if Book.query.filter_by(code=request.form["code"]).first():

            return redirect(url_for('add_book', error=True))

        new_book = Book(
            name=request.form['name'],
            code=request.form['code'],
            genre=request.form['genre'],
            author=request.form['author'],
            # _owner=add_book_form.owner.data,
        )
        db.session.add(new_book)
        db.session.commit()
        
        return redirect(url_for("add_book", success=True))
    
    return render_template("add-book.html")


@app.route('/delete', methods=["GET", "POST"])
def delete_book():

    if request.method == "POST":

        book = Book.query.filter_by(code=request.form['code']).first()

        if not book:
            return redirect(url_for('delete_book', error=True))

        else:
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('delete_book', success=True))
   
    return render_template("delete-book.html")


@app.route('/borrow', methods=["GET", "POST"])
def borrow_book():


    if request.method == "POST":
        code = request.form["code"]
        student_id = request.form["sid"]
        book_to_borrow = Book.query.filter_by(code=code).first()

        if book_to_borrow:

            student = Book.query.filter_by(holder=student_id).all()
            if len(student) < 3:
                book_to_borrow.holder = student_id
                db.session.commit()
                return redirect(url_for('borrow_book', success=True))

            return redirect(url_for('borrow_book', error=True))
    return render_template('borrow-book.html')


@app.route('/search', methods=["GET", "POST"])
def search_book():

    if request.method == "POST":
        if request.form['select'] == 'name':

            books = Book.query.filter_by(name=request.form['search']).all()
           
            return render_template("search_book.html", books=books)
        if request.form['select'] == 'code':

            books = Book.query.filter_by(code=request.form['search']).all()
            
            return render_template("search_book.html", books=books)
        if request.form['select'] == 'genre':

            books = Book.query.filter_by(genre=request.form['search']).all()
            
            return render_template("search_book.html", books=books)
        if request.form['select'] == 'author':

            books = Book.query.filter_by(author=request.form['search']).all()
            
            return render_template("search_book.html", books=books)
    return render_template("search_book.html")




if __name__ == "__main__":
    app.run(port=3000, debug=True)
