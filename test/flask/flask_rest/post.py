from flask import Flask, jsonify, abort, request
from appdef import app,books


@app.route('/bookstore/api/v1/books/', methods=['POST'])
def create_task():
    if not request.form or not 'title' in request.form:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.form['title'],
        'auther': request.form['auther'],
        'price': request.form['price'],
    }
    books.append(book)
    return jsonify({'book': book}), 201

@app.route('/bookstore/api/v1/books/<int:id>', methods=['PUT'])
def update_book(id):
    for book in books:
        if book['id']==id:
            book["title"] = request.form['title']
            book["auther"] = request.form['auther']
            book["price"] = request.form['price']
        return jsonify({'books': books})
    abort(400)


@app.route('/bookstore/api/v1/books/<int:id>', methods=['DELETE'])
def delete_task(id):
    for book in books:
        if book['id']==id:
            books.remove(book)
            return jsonify({'result': True})
    abort(404)

    return jsonify({'result': True})

