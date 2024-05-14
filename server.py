from flask import Flask, jsonify, request
import requests
from bson.objectid import ObjectId
import grpc
import books_pb2
import books_pb2_grpc

app = Flask(__name__, '/static')

# Connect to gRPC server
channel = grpc.insecure_channel('localhost:50051')
stub = books_pb2_grpc.BookServiceStub(channel)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/search')
def search_books():
    query = request.args.get('query')
    limit = int(request.args.get('limit', 10))
    page = int(request.args.get('page', 1))
    response = requests.get(f"https://openlibrary.org/search.json?q={query}&limit={limit}&page={page}")
    data = response.json()
    books = data.get('docs', [])
    return jsonify({'books': books})

@app.route('/add', methods=['POST'])
def add_book():
    book_data = request.json
    title = book_data.get('title')
    author = book_data.get('author')
    year = book_data.get('year')

    # Call gRPC method to add book
    response = stub.AddBook(books_pb2.AddBookRequest(book=books_pb2.Book(title=title, author=author, year=year)))
    return jsonify({'message': response.message})

@app.route('/list')
def list_books():
    books = stub.ListBooks(books_pb2.Empty())
    return jsonify({'books': [{'id': book.id, 'title': book.title, 'author': book.author, 'year': book.year} for book in books]})

@app.route('/update/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.json
    title = book_data.get('title')
    author = book_data.get('author')
    year = book_data.get('year')

    # Call gRPC method to update book
    response = stub.UpdateBook(books_pb2.UpdateBookRequest(id=book_id, book=books_pb2.Book(title=title, author=author, year=year)))
    return jsonify({'message': response.message})

@app.route('/delete/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    # Call gRPC method to delete book
    response = stub.DeleteBook(books_pb2.DeleteBookRequest(id=book_id))
    return jsonify({'message': response.message})

if __name__ == "__main__":
    app.run(port=5051)
