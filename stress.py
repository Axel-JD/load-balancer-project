import requests
import time
from colorama import init, Fore, Style

init(autoreset=True)

URL = "http://127.0.0.1:8080"
TOTAL_REQUESTS = 500 # Vamos fazer 100 disparos seguidos

print(f"{Fore.YELLOW}{Style.BRIGHT}=== INICIANDO TESTE DE ESTRESSE (DDOS SIMULADO) ==={Style.RESET_ALL}")
print(f"Alvo: {URL}")
print(f"Disparos: {TOTAL_REQUESTS}\n")

time.sleep(1)

start_time = time.time()
success_count = 0
error_count = 0

for i in range(1, TOTAL_REQUESTS + 1):
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"{Fore.GREEN}Request {i}/{TOTAL_REQUESTS}: OK", end="\r")
            success_count += 1
        else:
            print(f"{Fore.RED}Request {i}/{TOTAL_REQUESTS}: ERRO {response.status_code}", end="\r")
            error_count += 1
    except:
        print(f"{Fore.RED}Request {i}/{TOTAL_REQUESTS}: FALHA NA CONEXÃO", end="\r")
        error_count += 1

end_time = time.time()
duration = end_time - start_time
rps = TOTAL_REQUESTS / duration

print("\n\n" + "="*40)
print(f"{Fore.CYAN}RELATÓRIO DE PERFORMANCE")
print("="*40)
print(f"Tempo Total:      {duration:.2f} segundos")
print(f"Sucessos:         {Fore.GREEN}{success_count}")
print(f"Falhas:           {Fore.RED}{error_count}")
print(f"Velocidade:       {Fore.YELLOW}{rps:.2f} requisições/segundo")
print("="*40)

if rps > 50:
    print(f"{Fore.MAGENTA}CONCLUSÃO: O Cache está voando! 🚀")
else:
    print(f"{Fore.WHITE}CONCLUSÃO: Cache expirou ou desligado, processamento normal.")