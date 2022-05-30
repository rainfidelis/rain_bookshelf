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

        try:
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

    return app
