from app import create_app
from extensions import db
from models import Author, Genre, Book, Member, Loan

app = create_app()

with app.app_context():
    author = Author(name='Grace Hopper')
    db.session.add(author)

    genre = Genre(name='Ogre')
    db.session.add(genre)

    book = Book(title='The Friendly Ogre', author=author)
    book.genres.append(genre)
    db.session.add(book)

    member = Member(name='Naoimi')
    db.session.add(member)

    loan = Loan(book=book, member=member)
    db.session.add(loan)

    db.session.commit()

    print('Added test data: author, genre, book, member, loan')
