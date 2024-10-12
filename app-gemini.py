from flask import Flask, jsonify
import requests  # Biblioteca para chamadas HTTP
from flasgger import Swagger

app = Flask(__name__)

# Inicializar Swagger
swagger = Swagger(app)

# Novo endpoint que chama uma API externa
@app.route('/get-posts', methods=['GET'])
def get_posts():
    """
    Chama a API externa JSONPlaceholder e retorna os posts
    ---
    responses:
      200:
        description: Uma lista de posts vindos de uma API externa
        schema:
          type: array
          items:
            type: object
            properties:
              userId:
                type: integer
              id:
                type: integer
              title:
                type: string
              body:
                type: string
    """
    # Chama a API externa (JSONPlaceholder)
    response = requests.get('https://jsonplaceholder.typicode.com/posts')

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Retorna o JSON da resposta da API externa
        return jsonify(response.json())
    else:
        return jsonify({'error': 'Erro ao buscar dados da API externa'}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
