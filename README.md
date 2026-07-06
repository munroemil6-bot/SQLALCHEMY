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

Install dependencies (from the project folder):

```bash
cd project
python3 -m pip install -r requirements.txt
```

Run the app (creates the SQLite DB in `project/instance/library.db` and seeds example data):

```bash
cd project
python3 app.py
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

Start the shell from the project folder:

```bash
cd project
python3 -m flask shell
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

### Add or delete from any table

Use the same pattern for every model:

```python
# Create
new_item = Author(name='New Author')
db.session.add(new_item)
db.session.commit()

# Read by ID
item = Author.query.get(1)

# Update
if item:
    item.name = 'Updated Name'
    db.session.commit()

# Delete
if item:
    db.session.delete(item)
    db.session.commit()
```

You can replace `Author` with `Book`, `Genre`, `Member`, or `Loan`.

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

# First Time Setup (Only Once)

### 1. Initialize migrations

```bash
cd project
python3 -m flask db init
```

This creates:

```text
migrations/
    env.py
    script.py.mako
    versions/
```

You never run `flask db init` again for this project.

For this project, the earlier migration already exists and is stored in the migrations folder, so you can continue from the current setup.

# Creating the Database (First Migration)

Suppose your `models.py` currently contains:

```python
class Author(db.Model):
    ...

class Book(db.Model):
    ...

class Genre(db.Model):
    ...

class Member(db.Model):
    ...

class Loan(db.Model):
    ...
```

### 2. Generate a migration

```bash
cd project
python3 -m flask db migrate -m "Initial database"
```

Flask compares:

```text
models.py
        ↓
database
```

Since the database is empty, it creates instructions to build all the tables.

### 3. Apply the migration

```bash
cd project
python3 -m flask db upgrade
```

Now your SQLite database actually contains those tables.

For this project, the existing migration history is already in place and can be viewed with:

```bash
cd project
python3 -m flask db history
```

# Changing Your Database Later

Suppose your `Member` model was originally:

```python
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

Now you decide to add a phone number.

Change it to:

```python
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
```

Notice that you only edit the model. You do not write SQL.

### Generate another migration

```bash
cd project
python3 -m flask db migrate -m "Added phone to member"
```

Flask notices:

```text
Old Model

id
name

↓

New Model

id
name
phone
```

It creates a migration file containing the equivalent of:

```sql
ALTER TABLE member
ADD COLUMN phone;
```

### Apply it

```bash
cd project
python3 -m flask db upgrade
```

Done. Your existing members remain. Only the new column is added.

# What if I rename a column?

Suppose

```python
name = db.Column(db.String(100))
```

becomes

```python
full_name = db.Column(db.String(100))
```

Run

```bash
cd project
python3 -m flask db migrate -m "Rename member name"
```

Sometimes Flask-Migrate cannot automatically detect a rename. It may think:

- delete `name`
- create `full_name`

instead of renaming it.

In that case, you will need to edit the generated migration file manually before running `flask db upgrade`.

# Adding a New Model

Suppose you add:

```python
class Publisher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

Run:

```bash
cd project
python3 -m flask db migrate -m "Added publisher table"
```

Then:

```bash
cd project
python3 -m flask db upgrade
```

A new table is created without affecting the others.

# Changing a Relationship

Suppose you add:

```python
publisher_id = db.Column(
    db.Integer,
    db.ForeignKey("publisher.id")
)
```

Again:

```bash
cd project
python3 -m flask db migrate -m "Added publisher relationship"
```

Then:

```bash
cd project
python3 -m flask db upgrade
```

# Viewing Your Migration History

You can see all migrations:

```bash
cd project
python3 -m flask db history
```

Current migration:

```bash
cd project
python3 -m flask db current
```

# Going Back (Downgrade)

If something goes wrong:

```bash
cd project
python3 -m flask db downgrade
```

It undoes the last migration.

# Adding a New Column Through Migrations

If you want to add a new column to a table, edit the model first.

Example:

```python
class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
```

Then create and apply the migration:

```bash
cd project
python3 -m flask db migrate -m "Add email to member"
python3 -m flask db upgrade
```

After that, you can use the new column in the shell:

```bash
cd project
python3 -m flask shell
```

```python
member = Member.query.first()
member.email = 'myles@example.com'
db.session.commit()
```


