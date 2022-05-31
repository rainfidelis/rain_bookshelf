import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "RAIN", "RainBoy#$96", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys",
                         "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['books']))
        self.assertTrue(data['total_books'])

    def test_get_paginated_books_out_of_range(self):
        res = self.client().get('/books?page=100000')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")
        self.assertFalse(data['success'])

    def test_search_function(self):
        res = self.client().post("/books", json={"search": "Novel"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_search_function_empty_result(self):
        res = self.client().post("/books", json={"search": "applejacks"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(len(data['books']), 0)
        self.assertEqual(data['total_books'], 0)


    def test_update_book_rating(self):
        res = self.client().patch('/books/4', json={'rating': 2})
        data = json.loads(res.data)
        book = Book.query.get(4)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(book.rating, 2)

    def test_update_book_rating_no_data(self):
        res = self.client().patch('/books/4')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')


    def test_create_book(self):
        res = self.client().post('/books', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['books'])
        self.assertTrue(data['total_books'])

    def test_create_book_not_allowed(self):
        res = self.client().post('/books/50', json=self.new_book)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "method not allowed")

    def test_delete_book(self):
        res = self.client().delete('/books/32')
        data = json.loads(res.data)
        book = Book.query.get(27)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['books'])
        self.assertTrue(data['deleted'])
        self.assertTrue(data['total_books'])
        self.assertIsNone(book)

    def test_delete_book_404(self):
        res = self.client().delete('/books/500')
        data = json.loads(res.data)

        self.assertEqual(data['message'], "unprocessable")
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
