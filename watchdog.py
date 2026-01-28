import subprocess
import time
import sys
from colorama import init, Fore, Style

init(autoreset=True)

# Lista de portas que queremos manter vivas
PORTS = [8001, 8002, 8003]
processes = {} # Dicionário para guardar os processos {8001: processo, ...}

def start_server(port):
    """Inicia um servidor em segundo plano"""
    print(f"{Fore.CYAN}⚙️  Iniciando servidor na porta {port}...")
    
    # O comando equivale a digitar: python server.py <porta>
    # sys.executable garante que usamos o mesmo python que está rodando este script
    p = subprocess.Popen([sys.executable, "server.py", str(port)])
    return p

print(f"{Fore.YELLOW}{Style.BRIGHT}=== INICIANDO SISTEMA DE MONITORAMENTO (WATCHDOG) ==={Style.RESET_ALL}")
print("Este script vai garantir que os servidores 8001, 8002 e 8003 nunca morram.\n")

# 1. Start Inicial: Liga todos os servidores
for port in PORTS:
    processes[port] = start_server(port)

print(f"{Fore.GREEN}✔ Todos os servidores estão rodando. Monitorando...\n")

# 2. Loop Infinito de Monitoramento
try:
    while True:
        for port in PORTS:
            process = processes[port]
            
            # process.poll() retorna None se está vivo, ou um número se morreu
            if process.poll() is not None:
                print(f"{Fore.RED}{Style.BRIGHT}🚨 ALERTA: O servidor {port} CAIU! (Código: {process.returncode})")
                print(f"{Fore.YELLOW}♻️  Reiniciando servidor {port} imediatamente...")
                
                # Reinicia o servidor e atualiza o dicionário
                processes[port] = start_server(port)
                print(f"{Fore.GREEN}✔ Servidor {port} recuperado com sucesso!\n")
        
        # Espera 1 segundo antes de checar de novo (para não fritar o processador)
        time.sleep(1.5)

except KeyboardInterrupt:
    print(f"\n{Fore.WHITE}Desligando o Watchdog e matando todos os servidores...")
    for port, process in processes.items():
        process.terminate()
    print("Tchau!")