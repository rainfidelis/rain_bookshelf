import re
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Book

BOOKS_PER_SHELF = 8


def paginator(request, selection):

    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    formatted_books = [book.format() for book in selection]
    page_books = formatted_books[start:end]

    return page_books


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/books')
    def get_books():
        """
        Route to retrieve all books in a paginated manner. Max 8 books per page
        -----
        Returns: "Success", "Books", and "Total books"
        """
        all_books = Book.query.order_by(Book.id).all()
        page_books = paginator(request, all_books)

        if len(page_books) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "books": page_books,
            "total_books": len(all_books)
        })

    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_rating(book_id):
        """
        Patch method for updating the ratings of any selected book
        -----
        Returns "success" as response
        """
        body = request.get_json()

        book = Book.query.get(book_id)

        if book is None:
            abort(404)

        if 'rating' in body:
            book.rating = int(body["rating"])
            book.update()

            return jsonify({
                "success": True
            })
        else:
            abort(400)

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        try:
            if book is None:
                abort(404)

            book.delete()

            current_books = Book.query.order_by(Book.id).all()
            page_books = paginator(request, current_books)

            return jsonify({
                "success": True,
                "deleted": book_id,
                "books": page_books,
                "total_books": len(current_books)
            })

        except:
            abort(422)

    @app.route('/books', methods=['POST'])
    def create_book():
        body = request.get_json()

        title = body.get("title", None)
        author = body.get("author", None)
        rating = body.get("rating", None)
        search_term = body.get('search', None)

        try:
            if search_term:
                books = Book.query.filter(
                    Book.author.ilike(f'%{search_term}%') | 
                    Book.title.ilike(f'%{search_term}%')).all()
                found_books = paginator(request, books)

                return jsonify({
                    "success": True,
                    "books": found_books,
                    "total_books": len(found_books)
                    })
            else:
                new_book = Book(title=title, author=author, rating=rating)
                new_book.insert()

                all_books = Book.query.order_by(Book.id).all()
                page_books = paginator(request, all_books)

                return jsonify({
                    "success": True,
                    "created": new_book.id,
                    "books": page_books,
                    "total_books": len(all_books)
                })
        except:
            abort(422)

    # @app.route('/books/search', methods=['GET'])
    # def search_books():
    #     search_term = request.args.get('search')

    #     books = Book.query.filter(
    #         Book.author.ilike(f'%{search_term}%') | 
    #         Book.title.ilike(f'%{search_term}%')).all()
    #     found_books = [book.format() for book in books]

    #     return jsonify({
    #         "success": True,
    #         "books": found_books,
    #         "total_books": len(found_books)
    #         })
    
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404,)

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422,)

    @app.errorhandler(400)
    def bad_request(error):
        return (jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400,)

    @app.errorhandler(405)
    def not_allowed(error):
        return (jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405,)

    return app
