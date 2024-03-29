from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Book


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
app = Flask(__name__)
with app.app_context():
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

#----------------------------------------------------------------------------#
# Utility Function
#----------------------------------------------------------------------------#
BOOKS_PER_SHELF = 8

def paginator(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

# All Books
#----------------------------------------------------------------------------#
@app.route("/books")
def get_books():
    """
    Route to retrieve all books in a paginated manner. Max 8 books per page
    -----
    Returns: "Success", "Books", and "Total books"
    """
    selection = Book.query.order_by(-Book.id).all()
    current_books = paginator(request, selection)

    if len(current_books) == 0:
        abort(404)

    return jsonify(
        {
            "success": True,
            "books": current_books,
            "total_books": len(Book.query.all()),
        }
    )

# Update book detail
#----------------------------------------------------------------------------#
@app.route("/books/<int:book_id>", methods=["PATCH"])
def update_rating(book_id):
    """
    Patch method for updating the ratings of any selected book
    -----
    Returns "success" as response
    """
    body = request.get_json()

    try:
        book = Book.query.filter(Book.id == book_id).one_or_none()
        if book is None:
            abort(404)

        if "rating" in body:
            book.rating = int(body.get("rating"))

        book.update()

        return jsonify({"success": True, "id": book.id})

    except:
        abort(400)

# Delete Book
#----------------------------------------------------------------------------#
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    try:
        book = Book.query.filter(Book.id == book_id).one_or_none()

        if book is None:
            abort(404)

        book.delete()
        selection = Book.query.order_by(Book.id).all()
        current_books = paginator(request, selection)

        return jsonify(
            {
                "success": True,
                "deleted": book_id,
                "books": current_books,
                "total_books": len(Book.query.all()),
            }
        )

    except:
        abort(422)

# Create Book | Search Books
#----------------------------------------------------------------------------#
@app.route("/books", methods=["POST"])
def create_book():
    body = request.get_json()

    title = body.get("title", None)
    author = body.get("author", None)
    rating = body.get("rating", None)
    search = body.get("search", None)

    try:
        if search:
            selection = Book.query.order_by(Book.id).filter(
                Book.title.ilike(f"%{search}%") |
                Book.author.ilike(f"%{search}%")
            )
            current_books = paginator(request, selection)

            return jsonify(
                {
                    "success": True,
                    "books": current_books,
                    "total_books": len(selection.all()),
                }
            )
        else:
            book = Book(title=title, author=author, rating=rating)
            book.insert()

            selection = Book.query.order_by(Book.id).all()
            current_books = paginator(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": book.id,
                    "books": current_books,
                    "total_books": len(Book.query.all()),
                }
            )

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

# Error Handling
#----------------------------------------------------------------------------#
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
    }), 400)

@app.errorhandler(405)
def not_allowed(error):
    return (jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405,)

# Launch
#----------------------------------------------------------------------------#
if __name__=="__main__":
    app.run()
