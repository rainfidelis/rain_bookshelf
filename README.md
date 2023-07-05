# Virtual Bookshelf Project
![Bookshelf Image](/bookshelf_project.png)

The virtual bookshelf project is an online bookshelf simulator that plays host to some of the greatest books ever written (although the book contents aren't actually hosted for copyright reasons). 

The shelf presents books in a nice layout, with the book title, author, and rating all presented to the website visitor. 

It is a decoupled website project developed as a part of the Udacity Fullstack Nanodegree program, with a focus on API creation, testing, and documentation.

## Getting Started
To work with this project on your local device, you'll need to clone/fork the repository to your local device and install both the backend and frontend dependencies. You'll also need to already have Python3, pip and [node](https://nodejs.org/en/download/) installed on your local machine.

### Backend
After pulling the repo to your local machine, open your terminal and cd (change directory) into the backend directory of the repo. You'll have to install the dependencies from `requirements.txt` using either of:
- `pip install -r requirements.txt`, or
- `pipenv install -r requirements.txt` (for pipenv users)

Once the installation is complete, you can get your server running by running the following commands using PowerShell:
```
- $env:FLASK_APP = "flaskr"
- $env:FLASK_ENV = "development"
- flask run
```

For a Linux/Mac terminal, use the following commands instead:
```
- export FLASK_APP = "flaskr"
- export FLASK_ENV = "development"
- flask run
```
> The backend server is run on http://127.0.0.1:5000/ by default

### Frontend
With `npm` installed on your device, navigate into the frontend directory of the project repo and run the following commands to launch the react server:
```
- npm install
- npm start
```
> The frontend server runs on localhost:3000 or http://127.0.0.1:3000 

## Tests
In order to run tests navigate to the backend folder and run the following commands:
```
dropdb bookshelf_test
createdb bookshelf_test
psql bookshelf_test < books.psql
python tests.py
```

The first time you run the tests, omit the dropdb command.

All tests are kept in that file and should be maintained as updates are made to app functionality. 

## API Reference 
The Bookshelf API is a RESTful, resource-oriented API which returns JSON-encoded responses and uses standard HTTP response codes.

The API interacts with the bookshelf database, and helps users retrieve, post, or alter books in the bookshelf.

### Getting started
- Base URL: The API is currently only accessible via your localhost server and can be accessed locally via http://127.0.0.1:5000/ or localhost:5000
- Authentication: No authentication or API keys are required to access the API at this time.

### Error Handling
The Bookshelf API uses conventional HTTP response codes for successes and failures of API requests. As a reminder: Codes `2xx` indicate success, `4xx` indicate failures (such as a bad request or a request for non-existent data), and `5xx` indicate server errors (which means something went wrong with your local server). 

Errors are parsed back to the user as JSON-encoded messages in the format below:

    {
            "success": False,
            "error": 405,
            "message": "method not allowed"
    }

You can expect the following error codes when using the API:
+ `400 - Bad Request: The request wasn't accepted, often because of a missing parameter`
+ `404 - Not Found: The requested resource doesn't exist on the server`
+ `405 - Not Allowed: The request method isn't allowed for that endpoint`
+ `422 - Unprocessable: An error in your request is preventing the server from processing it`

### The Books Endpoint Library
This is an object representing individual books in the shelf. The book object indicates a book title, book author, and book rating. Each book is also assigned a unique ID for referencing the object.

### Retrieve Books Endpoint
Retrieves all books in the shelf and returns a paginated response, with 8 books per page. Takes the page number as a url argument, or defaults to page 1 if no page is passed.

```
GET /books

Sample Request:
    cURL http://127.0.0.1:5000/books?page=1

Parameters:
    None

Sample Response:
    {
        "success": True,
        "books": [{
                    "id": 1,
                    "title": The Great Alone,
                    "author": Kristin Hannah,
                    "rating": 4,
                },
                {
                    "id": 2,
                    "title": Lullaby,
                    "author": Leila Slimani,
                    "rating": 2,
                },
                {
                    "id": 3,
                    "title": Immigrant, Montana,
                    "author": Amitava Kumar,
                    "rating": 5,
                },
                {
                    "id": 4,
                    "title": All We Ever Wanted,
                    "author": Emily Giffin,
                    "rating": 4,
                },
                {
                    "id": 5,
                    "title": We Fed an Island,
                    "author": Jose Andres,
                    "rating": 4,
                }],
        "total_books": 5
    }
```

### Update Rating Endpoint
Updates the rating of a particular book and persists the new rating to the database. The book ID is required for a successful operation. Also required is a json body with the new rating.

```
PATCH /books/<int:book_id>

Sample Request:
    cURL http://127.0.0.1:5000/books/4

Parameters:
    json: {"rating": 3}

Sample Response:
    {
        "success": True, 
        "id": 4
    }

```

### Delete Book Endpoint
Deletes an existing book from the database. Requires an existing book ID for the operation to be successful.

```
DELETE /books/<int:book_id>

Sample Request:
    cURL http://127.0.0.1:5000/books/4

Parameters:
    None

Sample Response:
    {
        "success": True, 
        "deleted": 4,
        "books": [{
                    "id": 1,
                    "title": The Great Alone,
                    "author": Kristin Hannah,
                    "rating": 4,
                },
                {
                    "id": 2,
                    "title": Lullaby,
                    "author": Leila Slimani,
                    "rating": 2,
                },
                {
                    "id": 3,
                    "title": Immigrant, Montana,
                    "author": Amitava Kumar,
                    "rating": 5,
                },
                {
                    "id": 5,
                    "title": We Fed an Island,
                    "author": Jose Andres,
                    "rating": 4,
                }],
        "total_books": 4
    }

```

### Create Book Endpoint
Creates a new book object, assigns it a book ID, and persists it to the database. Takes a json body with the new book details.

```
POST /books

Sample Request:
    cURL http://127.0.0.1:5000/books

Parameters:
    json: {
            "title": "Inception", 
            "author": "John Codes",
            "rating": 4
          }

Response:
    {
        "success": True, 
        "created": 6,
        "books": [{
                    "id": 1,
                    "title": The Great Alone,
                    "author": Kristin Hannah,
                    "rating": 4,
                },
                {
                    "id": 2,
                    "title": Lullaby,
                    "author": Leila Slimani,
                    "rating": 2,
                },
                {
                    "id": 3,
                    "title": Immigrant, Montana,
                    "author": Amitava Kumar,
                    "rating": 5,
                },
                {
                    "id": 5,
                    "title": We Fed an Island,
                    "author": Jose Andres,
                    "rating": 4,
                },
                {
                    "id": 6,
                    "title": Inception,
                    "author": John Codes,
                    "rating": 4,
                }],
        "total_books": 5
    }

```
### Search Books Endpoint
Searches all existing books for books that match the search criteria in whole or part. Returns a paginated list of all books matching the search criteria. Receives the search parameter as a json body.

```
POST /books

Sample Request:
    cURL http://127.0.0.1:5000/books

Parameters:
    json: {"search": "fed"}

Response:
    {
        "success": True, 
        "books": [{
                    "id": 4,
                    "title": We Fed an Island,
                    "author": Jose Andres,
                    "rating": 4,
                 }]
        "total_books": 1
    }

```

## Authors
This project was authored by myself, [@rainfidelis](https://github.com/rainfidelis), as an extension of the original [Udacity provided repository](https://github.com/udacity/cd0037-API-Development-and-Documentation-exercises/tree/master/1_Requests_Starter).