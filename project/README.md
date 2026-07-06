# Project

Structure:

```
project/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── routes.py
├── templates/
├── instance/
├── migrations/
└── requirements.txt
```

Quick start

Prerequisites:
- Python 3.8+
- Create a virtualenv or use Pipenv

Install dependencies:

```bash
python3 -m pip install -r project/requirements.txt
```

Run the app (creates the SQLite DB in `project/instance/library.db` and seeds example data):

```bash
python3 project/app.py
```

Open http://127.0.0.1:5001/ in your browser.

Model relationships in this app:

- `Author` has many `Book` records.
- `Book` has one `Author` and many `Genre` records.
- `Genre` belongs to many `Book` records through `book_genre`.
- `Member` has many `Loan` records.
- `Loan` links one `Book` to one `Member`.


## Adding records with SQLAlchemy

When you create a Python object from a model, it exists only in memory until you save it.

Example:

```python
member = Member(
    name='Myles',
    # add more fields here if you extend the model
)

db.session.add(member)
db.session.commit()
```

The object:

```python
Member(
    name='Myles'
)
```

is not yet in the database. It is only in Python memory.

### What does `db.session.add()` do?

```python
db.session.add(member)
```

This tells SQLAlchemy:

> "I want this object saved."

Think of it like putting an item into a shopping cart. It has not been checked out yet.

### What does `db.session.commit()` do?

```python
db.session.commit()
```

This actually writes the data to the database.

Without `commit()`:

```python
member = Member(name='Myles')
db.session.add(member)
```

nothing is saved.

### Add data in the Flask shell

Start the shell:

```bash
cd project
flask shell
```

Then run these examples:

#### Add an Author

```python
author = Author(name='George R. R. Martin')
db.session.add(author)
db.session.commit()
```

#### Add a Genre

```python
genre = Genre(name='Historical Fiction')
db.session.add(genre)
db.session.commit()
```

#### Add a Book

```python
author = Author.query.filter_by(name='George R. R. Martin').first()
book = Book(title='A Song of Ice and Fire', author=author)
db.session.add(book)
db.session.commit()
```

#### Add a Member

```python
member = Member(name='Myles')
db.session.add(member)
db.session.commit()
```

#### Add a Loan

```python
book = Book.query.filter_by(title='A Song of Ice and Fire').first()
member = Member.query.filter_by(name='Myles').first()
loan = Loan(book=book, member=member)
db.session.add(loan)
db.session.commit()
```

#### Delete a record by ID

```python
author = Author.query.get(1)
if author:
    db.session.delete(author)
    db.session.commit()
    print('Deleted author')
else:
    print('Author not found')
```

You can delete other records the same way:

```python
book = Book.query.get(2)
if book:
    db.session.delete(book)
    db.session.commit()

genre = Genre.query.get(3)
if genre:
    db.session.delete(genre)
    db.session.commit()

loan = Loan.query.get(1)
if loan:
    db.session.delete(loan)
    db.session.commit()
```

Notes
- The app seeds example Authors, Genres, Books, Members, and a Loan on first run. Seeding is idempotent and will not create duplicates.
- Database file: `project/instance/library.db`.
- To change the port: `python3 project/app.py --port 8000` (or set `app.run(port=8000)` in `project/app.py`).

## Migrations (Version control for your database)

Migrations track changes to your database schema over time. Think of them as version control for your database structure, similar to Git for code.

### What are migrations?

Without migrations, you would need to write raw SQL:

```sql
ALTER TABLE book ADD COLUMN isbn VARCHAR(20);
```

With Flask-Migrate and SQLAlchemy, you simply change your model:

```python
class Book(db.Model):
    ...
    isbn = db.Column(db.String(20))
```

Then Flask-Migrate detects the change and creates a migration file automatically.

### How migrations work

1. **Initial setup** (one time):
   ```bash
   cd project
   python init_migrations.py
   ```

2. **Create a migration** (whenever you change a model):
   ```bash
   flask db migrate -m "Add ISBN to books"
   ```

   This creates a file in `migrations/versions/` that describes the schema change.

3. **Apply the migration** (update your database):
   ```bash
   flask db upgrade
   ```

### Example: Add an `email` field to Member

1. Modify `models.py`:
   ```python
   class Member(db.Model):
       id = db.Column(db.Integer, primary_key=True)
       name = db.Column(db.String(128), nullable=False)
       email = db.Column(db.String(120), unique=True)  # NEW
       loans = db.relationship('Loan', back_populates='member')
   ```

2. Create migration:
   ```bash
   flask db migrate -m "Add email to Member"
   ```

3. Apply migration:
   ```bash
   flask db upgrade
   ```

The migration is now tracked, and other developers or future versions of your app can run `flask db upgrade` to apply the same changes.

### Useful commands

```bash
# Show migration history
flask db history

# Downgrade to a previous version
flask db downgrade
```


