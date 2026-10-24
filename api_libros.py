from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "CCNA Routing and Switching", "author": "Cisco", "isbn": "9781587143878"},
    {"id": 2, "title": "DevNet Associate", "author": "Cisco", "isbn": "9780136642961"}
]

@app.route('/api/v1/books', methods=['GET'])
def get_books():
    sort_by = request.args.get('sort')
    if sort_by == 'author':
        sorted_books = sorted(books, key=lambda x: x['author'])
        return jsonify(sorted_books), 200
    return jsonify(books), 200

@app.route('/api/v1/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Libro no encontrado"}), 404

@app.route('/api/v1/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    books.append(new_book)
    return jsonify(new_book), 201

@app.route('/api/v1/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_data = request.get_json()
    for book in books:
        if book["id"] == book_id:
            book.update(updated_data)
            return jsonify(book), 200
    return jsonify({"error": "Libro no encontrado"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)