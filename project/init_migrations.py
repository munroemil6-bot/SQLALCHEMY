#!/usr/bin/env python
"""
Initialize Flask-Migrate for the project.
Run this once to set up the migrations system.
"""

import os
from app import create_app
from extensions import db, migrate
from models import Author, Genre, Book, Member, Loan

# Initialize app
app = create_app()

# Initialize migrations
migrate.init_app(app, db)

print("✓ Flask-Migrate initialized!")
print("\nNext steps:")
print("1. Create first migration: flask db migrate -m 'Initial migration'")
print("2. Apply migration:       flask db upgrade")
print("\nTo add changes later:")
print("- Modify your models in models.py")
print("- Run: flask db migrate -m 'Description of changes'")
print("- Apply: flask db upgrade")
