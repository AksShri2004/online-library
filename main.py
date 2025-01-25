from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


# all_books = []

class Base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"]  = "sqlite:///books.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    all_books = db.session.execute(db.select(Book)).scalars()
    return render_template("index.html", all_books = all_books)


@app.route("/add", methods =["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["title"],
            author=request.form["author"],
            rating=request.form["rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")

@app.route("/edit/<id>", methods= ["GET","POST"])
def edit_rating(id):
    book = db.get_or_404(Book, id)
    if request.method == "POST":
        book.rating = request.form["rating"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit-rating.html", book= book)

@app.route("/delete/<id>", methods = ["GET", "POST"])
def delete_rec(id):
    book = db.get_or_404(Book, id)

    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)

