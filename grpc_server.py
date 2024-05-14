import grpc
from concurrent import futures
import books_pb2
import books_pb2_grpc
from bson.objectid import ObjectId
from pymongo import MongoClient

# Initialize MongoDB client
client = MongoClient('mongodb://localhost:27017/')
db = client['library']
collection = db['use']

class BookService(books_pb2_grpc.BookServiceServicer):
    def AddBook(self, request, context):
        title = request.book.title
        author = request.book.author
        year = request.book.year

        # Insert into MongoDB
        book_id = collection.insert_one({
            'title': title,
            'author': author,
            'year': year
        }).inserted_id

        print(f"Added book: {title} by {author}, {year}")
        return books_pb2.AddBookResponse(message="Book added successfully")

    def ListBooks(self, request, context):
        books = []
        for book in collection.find():
            books.append(books_pb2.Book(
                id=str(book['_id']),
                title=book['title'],
                author=book['author'],
                year=book['year']
            ))
        return books_pb2.ListBooksResponse(books=books)

    def UpdateBook(self, request, context):
        book_id = ObjectId(request.id)
        title = request.book.title
        author = request.book.author
        year = request.book.year

        # Update in MongoDB
        collection.update_one({'_id': book_id}, {'$set': {
            'title': title,
            'author': author,
            'year': year
        }})

        print(f"Updated book with ID {book_id}")
        return books_pb2.UpdateBookResponse(message="Book updated successfully")

    def DeleteBook(self, request, context):
        book_id = ObjectId(request.id)

        # Delete from MongoDB
        collection.delete_one({'_id': book_id})

        print(f"Deleted book with ID {book_id}")
        return books_pb2.DeleteBookResponse(message="Book deleted successfully")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    books_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
