from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inicializar Swagger
swagger = Swagger(app)

# Modelo para os Livros
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Criar o banco de dados
with app.app_context():
    db.create_all()

# Rota para listar todos os livros
@app.route('/books', methods=['GET'])
def get_books():
    """
    Retorna a lista de todos os livros
    ---
    responses:
      200:
        description: Uma lista de livros
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                description: O ID do livro
              title:
                type: string
                description: O título do livro
              author:
                type: string
                description: O autor do livro
    """
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

# Rota para obter um livro específico por ID
@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    """
    Retorna um livro pelo ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: O ID do livro
    responses:
      200:
        description: Um livro
        schema:
          type: object
          properties:
            id:
              type: integer
              description: O ID do livro
            title:
              type: string
              description: O título do livro
            author:
              type: string
              description: O autor do livro
      404:
        description: Livro não encontrado
    """
    book = Book.query.get_or_404(id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

# Rota para criar um novo livro
@app.route('/books', methods=['POST'])
def add_book():
    """
    Adiciona um novo livro
    ---
    parameters:
      - name: book
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
    responses:
      201:
        description: Livro criado com sucesso
    """
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Livro criado com sucesso!'}), 201

# Rota para atualizar um livro
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    """
    Atualiza um livro existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: O ID do livro
      - name: book
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
            author:
              type: string
    responses:
      200:
        description: Livro atualizado com sucesso
      404:
        description: Livro não encontrado
    """
    data = request.get_json()
    book = Book.query.get_or_404(id)
    book.title = data['title']
    book.author = data['author']
    db.session.commit()
    return jsonify({'message': 'Livro atualizado com sucesso!'})

# Rota para deletar um livro
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    """
    Deleta um livro existente
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: O ID do livro
    responses:
      200:
        description: Livro deletado com sucesso
      404:
        description: Livro não encontrado
    """
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Livro deletado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
