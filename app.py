from flask import Flask
from flask_cors import CORS
from config import Config
from database import init_db
from api.routes import api_bp

def create_app():
    # Create and configure the Flask application.
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    init_db(app)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'name': 'Project Gutenberg Books API',
            'version': '1.0.0',
            'endpoints': {
                'books': '/api/v1/books',
                'book_detail': '/api/v1/books/{id}',
                'stats': '/api/v1/stats'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
