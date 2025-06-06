from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Função para iniciar o banco de dados
def init_db():
    try:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS livros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    categoria TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    imagemUrl TEXT NOT NULL
                )
            """)
            print("Banco de dados inicializado com sucesso! ✅")
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")

init_db()

@app.route('/')
def homepage():
    return "<h3>Minha página usando Flask</h3>"

@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()
    campos_obrigatorios = ['titulo', 'categoria', 'autor', 'imagemUrl']
    
    # Verifica quais campos estão faltando
    campos_faltando = [campo for campo in campos_obrigatorios if campo not in dados]
    
    if campos_faltando:
        return jsonify({'erro': f'Campos obrigatórios ausentes: {", ".join(campos_faltando)}'}), 400

    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO livros (titulo, categoria, autor, imagemUrl)
            VALUES (?, ?, ?, ?)
        """, (dados['titulo'], dados['categoria'], dados['autor'], dados['imagemUrl']))
        conn.commit()

    return jsonify({'mensagem': 'Livro cadastrado com sucesso'}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros")
        livros = cursor.fetchall()

    livros_lista = [
        {'id': livro[0], 'titulo': livro[1], 'categoria': livro[2],
         'autor': livro[3], 'imagemUrl': livro[4]}
        for livro in livros
    ]

    return jsonify(livros_lista)

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
            'imagemUrl': livro[4]
        }
        return jsonify(livro_detalhes)
    else:
        return jsonify({'erro': 'Livro não encontrado'}), 404

@app.route('/livros/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM livros WHERE id = ?", (id,))
        livro = cursor.fetchone()

        if livro:
            cursor.execute("DELETE FROM livros WHERE id = ?", (id,))
            conn.commit()
            return jsonify({'mensagem': 'Livro deletado com sucesso'}), 200
        else:
            return jsonify({'erro': 'Livro não encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)