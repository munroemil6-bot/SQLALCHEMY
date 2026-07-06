import os
from flask import Flask
from config import Config
from extensions import db, migrate
from models import Author, Genre, Book, Member, Loan


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        os.makedirs(app.instance_path, exist_ok=True)
        db.create_all()
        seed_data()

        from routes import bp
        app.register_blueprint(bp)

    return app


def seed_data():
    # idempotent get-or-create helpers
    def get_or_create(model, defaults=None, **kwargs):
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            return instance
        params = dict((k, v) for k, v in kwargs.items())
        if defaults:
            params.update(defaults)
        instance = model(**params)
        db.session.add(instance)
        db.session.flush()
        return instance

    a1 = get_or_create(Author, name='J. R. R. Tolkien')
    a2 = get_or_create(Author, name='George Orwell')
    a3 = get_or_create(Author, name='Jane Austen')
    a4 = get_or_create(Author, name='Suzanne Collins')

    g1 = get_or_create(Genre, name='Fantasy')
    g2 = get_or_create(Genre, name='Dystopian')
    g3 = get_or_create(Genre, name='Adventure')
    g4 = get_or_create(Genre, name='Romance')
    g5 = get_or_create(Genre, name='Science Fiction')

    books = [
        {
            'title': 'The Hobbit',
            'author': a1,
            'genres': [g1, g3]
        },
        {
            'title': '1984',
            'author': a2,
            'genres': [g2]
        },
        {
            'title': 'The Lord of the Rings',
            'author': a1,
            'genres': [g1, g3]
        },
        {
            'title': 'Pride and Prejudice',
            'author': a3,
            'genres': [g4]
        },
        {
            'title': 'The Hunger Games',
            'author': a4,
            'genres': [g2, g5]
        },
        {
            'title': 'Animal Farm',
            'author': a2,
            'genres': [g2]
        },
    ]

    book_objects = {}
    for book_data in books:
        book = Book.query.filter_by(title=book_data['title']).first()
        if not book:
            book = Book(title=book_data['title'], author=book_data['author'])
            db.session.add(book)
            db.session.flush()
        for genre in book_data['genres']:
            if genre not in book.genres:
                book.genres.append(genre)
        book_objects[book_data['title']] = book

    m1 = get_or_create(Member, name='Alice')
    m2 = get_or_create(Member, name='Bob')
    m3 = get_or_create(Member, name='Charlie')
    m4 = get_or_create(Member, name='Dana')
    m5 = get_or_create(Member, name='Eve')

    loans = [
        {'book': book_objects['The Hobbit'], 'member': m1},
        {'book': book_objects['1984'], 'member': m2},
        {'book': book_objects['Pride and Prejudice'], 'member': m3},
        {'book': book_objects['The Hunger Games'], 'member': m4},
    ]

    for loan_data in loans:
        loan = Loan.query.filter_by(book_id=loan_data['book'].id, member_id=loan_data['member'].id).first()
        if not loan:
            loan = Loan(book=loan_data['book'], member=loan_data['member'])
            db.session.add(loan)

    db.session.commit()


if __name__ == '__main__':
    import os
    import sys

    app = create_app()
    # determine port: CLI --port N or PORT env var, default 5000
    port = 500
    for i, a in enumerate(sys.argv):
        if a in ('--port', '-p') and i + 1 < len(sys.argv):
            try:
                port = int(sys.argv[i + 1])
            except ValueError:
                pass
    port = int(os.environ.get('PORT', port))
    app.run(debug=True, port=port)
