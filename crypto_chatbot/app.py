import requests
from flask import Flask, jsonify, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Mantenha essa chave em segredo

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin):
    def __init__(self, id):
        self.id = id


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


# Simulando um banco de dados de usuários
users = {'admin': 'password123'}


@app.route('/')
@login_required
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            user = User(id=username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Credenciais inválidas')
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Usuário já existe')
        users[username] = password
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/api/bitcoin-price', methods=['GET'])
@login_required
def get_bitcoin_price():
    try:
        response = requests.get('https://api.gemini.com/v1/pubticker/btcusd')
        response.raise_for_status()  # Levanta um erro se a resposta for um código de status 4xx ou 5xx
        data = response.json()
        price_usd = float(data['last'])
        return jsonify({'price_usd': price_usd}), 200
    except requests.RequestException:
        return jsonify({'error': 'Não foi possível obter o preço do Bitcoin'}), 500


@app.route('/api/convert', methods=['GET'])
@login_required
def convert_currency():
    target_currency = request.args.get('currency', 'EUR').upper()  # Moeda padrão: EUR
    try:
        response = requests.get(
            f'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies={target_currency}')
        response.raise_for_status()
        data = response.json()
        price_in_target_currency = data['bitcoin'][target_currency.lower()]
        return jsonify({'price': price_in_target_currency}), 200
    except (requests.RequestException, KeyError):
        return jsonify({'error': 'Não foi possível obter a taxa de câmbio'}), 500


@app.route('/chat', methods=['POST'])
@login_required
def chat():
    user_message = request.json.get('message', '')

    # Removido o código relacionado às novas moedas

    return jsonify({'response': "Desculpe, não entendi sua pergunta."})


if __name__ == '__main__':
    app.run(debug=True)
