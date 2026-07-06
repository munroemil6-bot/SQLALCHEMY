from flask import Blueprint, render_template
from models import Author, Genre, Book, Member, Loan

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    authors = Author.query.all()
    genres = Genre.query.all()
    books = Book.query.all()
    members = Member.query.all()
    loans = Loan.query.all()
    return render_template('index.html', authors=authors, genres=genres, books=books, members=members, loans=loans)
