from database import db
from sqlalchemy import func

class Book(db.Model):
    # Book model representing Project Gutenberg books
    
    __tablename__ = 'books_book'
    
    id = db.Column(db.Integer, primary_key=True)
    download_count = db.Column(db.Integer)
    gutenberg_id = db.Column(db.Integer, nullable=False)
    media_type = db.Column(db.String(16), nullable=False)
    title = db.Column(db.String(1024))
    
    # Relationships
    authors = db.relationship('Author', secondary='books_book_authors', 
                            backref='books', lazy='joined')
    languages = db.relationship('Language', secondary='books_book_languages',
                              backref='books', lazy='joined')
    subjects = db.relationship('Subject', secondary='books_book_subjects',
                             backref='books', lazy='joined')
    bookshelves = db.relationship('Bookshelf', secondary='books_book_bookshelves',
                                backref='books', lazy='joined')
    formats = db.relationship('Format', backref='book', lazy='joined')
    
    def to_dict(self):
    #    Convert book object to dictionary for JSON response.
        return {
            'id': self.gutenberg_id,  # Return gutenberg_id as the main ID
            'title': self.title,
            'authors': [author.to_dict() for author in self.authors],
            'languages': [lang.code for lang in self.languages],
            'subjects': [subject.name for subject in self.subjects],
            'bookshelves': [shelf.name for shelf in self.bookshelves],
            'download_links': {
                format.mime_type: format.url for format in self.formats
            }
        }


class Author(db.Model):
    # Author model.
    
    __tablename__ = 'books_author'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    birth_year = db.Column(db.Integer)
    death_year = db.Column(db.Integer)
    
    def to_dict(self):
        """Convert author object to dictionary."""
        return {
            'name': self.name,
            'birth_year': self.birth_year,
            'death_year': self.death_year
        }


class Language(db.Model):
    # Language model.
    
    __tablename__ = 'books_language'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))


class Subject(db.Model):
    # Subject model.
    
    __tablename__ = 'books_subject'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Bookshelf(db.Model):
    # Bookshelf model.
    
    __tablename__ = 'books_bookshelf'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Format(db.Model):
    # Format model for book download links.
    
    __tablename__ = 'books_format'
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books_book.id'))
    mime_type = db.Column(db.String(50))
    url = db.Column(db.String(512))


# Association tables
books_authors = db.Table('books_book_authors',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('books_author.id'))
)

books_languages = db.Table('books_book_languages',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('books_language.id'))
)

books_subjects = db.Table('books_book_subjects',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.id')),
    db.Column('subject_id', db.Integer, db.ForeignKey('books_subject.id'))
)

books_bookshelves = db.Table('books_book_bookshelves',
    db.Column('book_id', db.Integer, db.ForeignKey('books_book.id')),
    db.Column('bookshelf_id', db.Integer, db.ForeignKey('books_bookshelf.id'))
)