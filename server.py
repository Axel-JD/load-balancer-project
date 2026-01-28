from flask import Flask, render_template # Importamos render_template
import sys
import os

# O Flask já sabe procurar nas pastas 'templates' e 'static' automaticamente
app = Flask(__name__)
port = int(sys.argv[1])

@app.route('/')
def home():
    # Em vez de texto puro, renderizamos o HTML.
    # Passamos a variável 'port' para dentro do HTML com o nome 'server_port'
    return render_template('index.html', server_port=port)

# Rota de sabotagem (mantive para sua apresentação)
@app.route('/kill')
def kill():
    print(f"💀 Servidor {port} cometendo suicídio digital...")
    os._exit(1) 

if __name__ == '__main__':
    # debug=False é importante para produção, mas para testes pode ser True
    app.run(port=port, threaded=True, debug=False)