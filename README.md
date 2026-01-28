# load-balancer-project
apenas um projeto simples de vibe coding vendo o que eu conseguia fazer com um servidor local e tentativa de logins, proteção contra ddos, etc.

Para iniciar o projeto apenas abra dois CMD a partir da pasta onde está os arquivos, em um deles escreva "python balancer.py" e no outro "python watchdog.py".
Depois é só entrar no navegador de preferencia e acessar "http://localhost:8080/login".

Se quiser pode usar os outros arquivos testes que eu utilizava no inicio como o client, server e stress.py, para abrir os servidores apenas use "python client.py 8001/8002/8003", após isso pode usar o client.py para que seja feito requisições a cada poucos segundos. Você recebera uma mensagem no CMD com o balancer ativado se a requisição foi bem sucedida ou não. (Cada um doss arquivos precisa ser aberto em sua própria janela do CMD).
