from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('emails.db')  # Conecta ou cria o arquivo do banco de dados
# Cria a tabela se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS unsubscribed_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            unsubscribed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Rota para descadastrar
@app.route('/unsubscribe', methods=['GET'])
def unsubscribe():
    email = request.args.get('email')  # Obtém o e-mail da URL
    if email:
        # Salva o e-mail em um arquivo .txt
        with open('unsubscribed_emails.txt', 'a') as file:
            file.write(f"{email}\n")

        # Salva o e-mail no banco de dados
        try:
            conn = sqlite3.connect('emails.db')  # Conecta ao banco de dados
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO unsubscribed_emails (email) VALUES (?)
            ''', (email,))
            conn.commit()
            conn.close()
            return f"Seu e-mail ({email}) foi descadastrado com sucesso!", 200
        except sqlite3.IntegrityError:
            return f"Seu e-mail ({email}) já foi descadastrado anteriormente.", 200
        except Exception as e:
            return f"Erro ao processar sua solicitação: {e}", 500

    return "E-mail inválido ou não fornecido.", 400

if __name__ == "__main__":
    # Inicializa o banco de dados antes de iniciar o app
    init_db()
    app.run(debug=True)
