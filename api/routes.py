from flask import Blueprint, request, jsonify
from sqlalchemy import distinct
from models import Book, Author, Language, Subject, Bookshelf, db
from api.utils import apply_filters, format_response
from config import Config

api_bp = Blueprint('api', __name__)

@api_bp.route('/books', methods=['GET'])
def get_books():
    """
    - id: Comma-separated list of Project Gutenberg book IDs
    - language: Comma-separated list of language codes (e.g., 'en,fr')
    - mime_type: Comma-separated list of mime types
    - topic: Comma-separated list of topics
    - author: Comma-separated list of author names
    - title: Comma-separated list of title keywords
    - page: Page number for pagination
    
    Returns:
    JSON response with book count and list of books
    """
    try:
        # Get query parameters
        filters = {
            'id': request.args.get('id'),
            'language': request.args.get('language'),
            'mime_type': request.args.get('mime_type'),
            'topic': request.args.get('topic'),
            'author': request.args.get('author'),
            'title': request.args.get('title')
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = Config.BOOKS_PER_PAGE
        
        # Build query
        query = Book.query.distinct()
        
        # Apply filters
        query = apply_filters(query, filters)
        
        # Get total count before pagination
        total_count = query.count()
        
        query = query.order_by(Book.download_count.desc().nullslast())
        
        # Apply pagination
        books = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        ).items
        
        # Format response
        response = format_response(books, total_count, page, per_page)
        
        return jsonify(response), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while processing your request',
            'message': str(e)
        }), 500


@api_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Get a specific book by Gutenberg ID.
    
    Parameters:
    - book_id: Project Gutenberg book ID
    
    Returns:
    JSON response with book details
    """
    try:
        book = Book.query.filter_by(gutenberg_id=book_id).first()
        
        if not book:
            return jsonify({
                'error': 'Book not found',
                'message': f'No book found with Gutenberg ID {book_id}'
            }), 404
        
        return jsonify(book.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while retrieving the book',
            'message': str(e)
        }), 500


@api_bp.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics."""
    try:
        stats = {
            'total_books': Book.query.count(),
            'total_authors': db.session.query(distinct(Author.id)).count(),
            'total_languages': db.session.query(distinct(Language.id)).count(),
            'total_subjects': db.session.query(distinct(Subject.id)).count(),
            'total_bookshelves': db.session.query(distinct(Bookshelf.id)).count()
        }
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': 'An error occurred while retrieving statistics',
            'message': str(e)
        }), 500
