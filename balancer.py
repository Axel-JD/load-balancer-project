from flask import Flask, request, render_template, make_response, session, redirect, url_for
import requests
import time
import json
import os
from colorama import init, Fore, Style

init(autoreset=True)
app = Flask(__name__)

# --- CONFIGURAÇÃO DE SESSÃO ---
# Necessário para o Flask lembrar quem está logado (criptografia do cookie)
app.secret_key = 'super_senha_secreta_do_projeto' 

# --- CONFIGURAÇÃO DO PROJETO ---
SERVERS = ['http://127.0.0.1:8001', 'http://127.0.0.1:8002', 'http://127.0.0.1:8003']
current_index = 0
cache_memory = {}
CACHE_TIMEOUT = 5 
request_history = {}
MAX_REQUESTS = 5 
TIME_WINDOW = 10 
DB_FILE = 'users.json'

# --- FUNÇÕES AUXILIARES ---
def load_users():
    """Lê o arquivo JSON de usuários"""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_user(username, password):
    """Salva um novo usuário no JSON"""
    users = load_users()
    users[username] = password
    with open(DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def check_rate_limit(ip):
    current_time = time.time()
    if ip not in request_history:
        request_history[ip] = []
    request_history[ip] = [t for t in request_history[ip] if current_time - t < TIME_WINDOW]
    request_history[ip].append(current_time)
    return len(request_history[ip]) <= MAX_REQUESTS

# --- ROTAS DE AUTENTICAÇÃO (LOGIN/REGISTER) ---

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        action = request.form['action'] # Descobre se é Login ou Cadastrar
        
        db = load_users()

        if action == 'register':
            if user in db:
                error = "Usuário já existe!"
            else:
                save_user(user, pwd)
                session['user'] = user # Loga automaticamente
                return redirect('/painel')
        
        elif action == 'login':
            if user in db and db[user] == pwd:
                session['user'] = user # Salva na sessão
                return redirect('/painel')
            else:
                error = "Usuário ou senha incorretos."

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('user', None) # Remove o usuário da sessão
    return redirect('/login')

# --- ROTAS DO SISTEMA ---

@app.route('/painel')
def dashboard():
    # Proteção: Se não estiver logado, manda pro login
    if 'user' not in session:
        return redirect('/login')
    
    # Passamos o nome do usuário para o HTML
    return render_template('dashboard.html', username=session['user'])

@app.route('/')
def proxy():
    # ... (Sua lógica original do Load Balancer continua igual aqui) ...
    # Se quiser forçar login até pra ver o site, descomente as linhas abaixo:
    # if 'user' not in session:
    #     return redirect('/login')

    global current_index
    client_ip = request.remote_addr 

    if not check_rate_limit(client_ip):
        return render_template('429.html'), 429

    cache_key = 'home_page'
    current_time = time.time()
    
    # Lógica de Cache
    if cache_key in cache_memory:
        saved = cache_memory[cache_key]
        if current_time - saved['time'] < CACHE_TIMEOUT:
            resp = make_response(saved['content'])
            resp.headers['X-Server-ID'] = 'CACHE'
            return resp

    # Lógica de Backend
    attempts = 0
    while attempts < len(SERVERS):
        server_url = SERVERS[current_index]
        current_index = (current_index + 1) % len(SERVERS)
        try:
            r = requests.get(server_url, timeout=2)
            cache_memory[cache_key] = {'content': r.text, 'time': time.time()}
            resp = make_response(r.text)
            port = server_url.split(':')[-1]
            resp.headers['X-Server-ID'] = port 
            return resp
        except:
            attempts += 1
            
    return "Serviço Indisponível", 503

if __name__ == '__main__':
    app.run(port=8080, threaded=True)