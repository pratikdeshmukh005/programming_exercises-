from typing import List, Dict, Any
from sqlalchemy import or_, and_, func
from models import Book, Author, Language, Subject, Bookshelf, Format

def parse_filter_values(value: str) -> List[str]:
    # Parse comma-separated filter values.
    if not value:
        return []
    return [v.strip() for v in value.split(',') if v.strip()]


def apply_filters(query, filters: Dict[str, Any]):    
    # Filter by gutenberg IDs
    if 'id' in filters:
        ids = parse_filter_values(filters['id'])
        if ids:
            query = query.filter(Book.gutenberg_id.in_([int(id) for id in ids if id.isdigit()]))
    
    # Filter by languages
    if 'language' in filters:
        languages = parse_filter_values(filters['language'])
        if languages:
            query = query.join(Book.languages).filter(
                Language.code.in_(languages)
            )
    
    # Filter by mime-type
    if 'mime_type' in filters:
        mime_types = parse_filter_values(filters['mime_type'])
        if mime_types:
            query = query.join(Book.formats).filter(
                Format.mime_type.in_(mime_types)
            )
    
    # Filter by topic (subjects or bookshelves)
    if 'topic' in filters:
        topics = parse_filter_values(filters['topic'])
        if topics:
            topic_conditions = []
            for topic in topics:
                topic_pattern = f'%{topic}%'
                topic_conditions.append(
                    or_(
                        Book.subjects.any(Subject.name.ilike(topic_pattern)),
                        Book.bookshelves.any(Bookshelf.name.ilike(topic_pattern))
                    )
                )
            query = query.filter(or_(*topic_conditions))
    
    # Filter by author
    if 'author' in filters:
        authors = parse_filter_values(filters['author'])
        if authors:
            author_conditions = []
            for author in authors:
                author_pattern = f'%{author}%'
                author_conditions.append(
                    Book.authors.any(Author.name.ilike(author_pattern))
                )
            query = query.filter(or_(*author_conditions))
    
    # Filter by title
    if 'title' in filters:
        titles = parse_filter_values(filters['title'])
        if titles:
            title_conditions = []
            for title in titles:
                title_pattern = f'%{title}%'
                title_conditions.append(Book.title.ilike(title_pattern))
            query = query.filter(or_(*title_conditions))
    
    return query


def format_response(books: List[Book], total_count: int, page: int, 
                   per_page: int) -> Dict[str, Any]:
    # Format the API response.
    return {
        'count': total_count,
        'page': page,
        'total_pages': (total_count + per_page - 1) // per_page,
        'books': [book.to_dict() for book in books]
    }
