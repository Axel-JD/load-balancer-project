import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)

URL = "http://127.0.0.1:8080"

print(f"{Fore.CYAN}=== INICIANDO SIMULAÇÃO DE TRÁFEGO ==={Style.RESET_ALL}")
print("Pressione CTRL+C para parar.\n")

user_id = 1

while True:
    try:
        print(f"{Fore.WHITE}Usuário {user_id} acessando o site...", end=" ")
        
        # Faz a requisição
        response = requests.get(URL)
        
        if response.status_code == 200:
            # Limpa o texto da resposta para ficar bonito
            server_msg = response.text.replace("Olá! Eu sou o ", "")
            print(f"{Fore.GREEN}✔ SUCESSO! Atendido por: {Style.BRIGHT}{server_msg}")
        else:
            print(f"{Fore.RED}✖ ERRO {response.status_code}: Serviço Indisponível")
            
    except Exception as e:
        print(f"{Fore.RED}✖ ERRO DE CONEXÃO: O Load Balancer não respondeu.")
    
    user_id += 1
    time.sleep(5) # Espera o número de segundos entre clientes