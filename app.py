from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para iniciar o banco de dados
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         titulo TEXT NOT NULL,
                         categoria TEXT NOT NULL,
                         autor TEXT NOT NULL,
                         imagem_url TEXT NOT NULL
                         )""")
        print("Banco de dados inicializado com sucesso! ✅")

init_db()

@app.route('/')
def homepage():
    return "<h3>Minha página usando Flask</h3>"

@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()
    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({'erro': 'todos os campos sao obrigatorios'}), 400

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO livros (titulo, categoria, autor, imagem_url)
            VALUES (?, ?, ?, ?)
        """, (titulo, categoria, autor, imagem_url))

        conn.commit()

    return jsonify({'mensagem': 'livro cadastrado com sucesso'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()

    livros_lista = [
        {'id': livro[0], 'titulo': livro[1], 'categoria': livro[2],
            'autor': livro[3], 'imagem_url': livro[4]}
        for livro in livros
    ]

    return jsonify(livros_lista)

# Nova rota para obter um livro específico pelo ID
@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
        livro = cursor.fetchone()

    if livro:
        livro_detalhes = {
            'id': livro[0],
            'titulo': livro[1],
            'categoria': livro[2],
            'autor': livro[3],
            'imagem_url': livro[4]
        }
        return jsonify(livro_detalhes)
    else:
        return jsonify({'erro': 'Livro não encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True)
