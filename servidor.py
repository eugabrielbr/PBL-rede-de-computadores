import socket
import pickle
from cliente import Cliente

clientes_conectados = []

trechos_viagem = {
    "São Paulo, SP": {
        "Rio de Janeiro, RJ": {"distancia": 430, "vagas": 0, "preco": 120},
        "Belo Horizonte, MG": {"distancia": 586, "vagas": 8, "preco": 150}
    },
    "Rio de Janeiro, RJ": {
        "São Paulo, SP": {"distancia": 430, "vagas": 5, "preco": 120},
        "Brasília, DF": {"distancia": 1148, "vagas": 3, "preco": 250}
    },
    "Brasília, DF": {
        "Rio de Janeiro, RJ": {"distancia": 1148, "vagas": 1, "preco": 250},
        "Salvador, BA": {"distancia": 1440, "vagas": 6, "preco": 300}
    },
    "Salvador, BA": {
        "Brasília, DF": {"distancia": 1440, "vagas": 6, "preco": 300},
        "Fortaleza, CE": {"distancia": 1023, "vagas": 4, "preco": 220}
    },
    "Fortaleza, CE": {
        "Salvador, BA": {"distancia": 1023, "vagas": 4, "preco": 220},
        "Recife, PE": {"distancia": 800, "vagas": 10, "preco": 180}
    },
    "Belo Horizonte, MG": {
        "São Paulo, SP": {"distancia": 586, "vagas": 8, "preco": 150},
        "Porto Alegre, RS": {"distancia": 1712, "vagas": 7, "preco": 400}
    },
    "Recife, PE": {
        "Fortaleza, CE": {"distancia": 800, "vagas": 10, "preco": 180},
        "Manaus, AM": {"distancia": 2714, "vagas": 2, "preco": 600}
    },
    "Porto Alegre, RS": {
        "Belo Horizonte, MG": {"distancia": 1712, "vagas": 7, "preco": 400},
        "Curitiba, PR": {"distancia": 711, "vagas": 9, "preco": 100}
    },
    "Curitiba, PR": {
        "Porto Alegre, RS": {"distancia": 711, "vagas": 9, "preco": 100},
        "São Paulo, SP": {"distancia": 408, "vagas": 5, "preco": 90}
    },
    "Manaus, AM": {
        "Recife, PE": {"distancia": 2714, "vagas": 2, "preco": 600},
        "Brasília, DF": {"distancia": 1930, "vagas": 6, "preco": 500}
    }
}

def retornar_trechos():
    """Retorna o dicionário de trechos de viagem."""
    return trechos_viagem

def editar_trecho(caminho, trechosviagem):
    trecho = caminho["caminho"]
    print(trechosviagem[trecho[0]][trecho[1]]["vagas"])
    while len(trecho) > 1:
        if trechosviagem[trecho[0]][trecho[1]]["vagas"] > 0:
            trechosviagem[trecho[0]][trecho[1]]["vagas"] -= 1
            print(trechosviagem[trecho[0]][trecho[1]]["vagas"])
            trecho.pop(0)
        elif trechosviagem[trecho[0]][trecho[1]]["vagas"] < 1:
            return False
    return trechosviagem

def busca_possibilidades(grafo, origem, destino):
    """Busca todas as possibilidades de rotas de origem a destino, incluindo o preço total."""
    rotas = {}
    id_rota = 1

    def dfs(cidade_atual, caminho, visitados, preco_total):
        nonlocal id_rota
        caminho.append(cidade_atual)
        visitados.add(cidade_atual)

        if cidade_atual == destino:
            rotas[id_rota] = {"caminho": caminho[:], "preco_total": preco_total}
            id_rota += 1
        else:
            for vizinho, info in grafo.get(cidade_atual, {}).items():
                if info["vagas"] > 0 and vizinho not in visitados:
                    # Somar o preço da viagem atual ao preço total
                    dfs(vizinho, caminho[:], visitados, preco_total + info["preco"])

        caminho.pop()
        visitados.remove(cidade_atual)

    dfs(origem, [], set(), 0)
    return rotas

def start_server(host='localhost', port=1080):
    """Inicia o servidor para aceitar conexões de clientes e processar dados."""
    trechosviagem = trechos_viagem
    cliente_conectado = Cliente(0)
    clientes_conectados.append("12345") #isso aq é para testar caso um cpf ja esteja logado 
    
    
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind((host, port))
        socket_server.listen(5)
        print(f"Disponível em {host}:{port}")



        while True: 
            client_socket, client_address = socket_server.accept()
            print(f"Conectado com {client_address}")
            # Recebendo dados de login:
            try:
                data_login = client_socket.recv(4096)
                obj_login = pickle.loads(data_login)

                # Se o cliente já está conectado em outro IP ou no mesmo, ele é desconectado
                if obj_login.cpf in clientes_conectados:
                    client_socket.sendall(pickle.dumps(False))
                    print(f"conexao com {obj_login.cpf} negada. Motivo: mais de um cpf igual conectado")
                    client_socket.close()
                    block = False 
                    
                else:
                    client_socket.sendall(pickle.dumps(True))
                    print(f"conexao com o cliente {obj_login.cpf} estabelecida")
                    cliente_conectado = obj_login
                    clientes_conectados.append(cliente_conectado.cpf)
                    block = True

            except (pickle.PickleError, socket.error) as e:
                print(f"Erro na comunicação conc: {e}")

            if block:
                while True:
                    try:
                        data = client_socket.recv(4096)
                        if not data:
                            break

                        obj = pickle.loads(data)
                        print(f"Dados recebidos: {obj}")

                        if obj == "trechos":
                            new_obj = trechosviagem
                        elif obj[0] == "compra":
                            trechosviagem = editar_trecho(obj[1], trechosviagem)
                        else:
                            cidade1, cidade2 = obj
                            new_obj = busca_possibilidades(trechosviagem, cidade1, cidade2)

                        data_send = pickle.dumps(new_obj)
                        client_socket.sendall(data_send)

                    except (pickle.PickleError, socket.error) as e:
                        print(f"Erro na comunicação: {e}")
                        break

                    
                print(clientes_conectados)
                if cliente_conectado.cpf in clientes_conectados:
                    client_socket.close() 
                    clientes_conectados.remove(cliente_conectado.cpf)
                print(clientes_conectados)
                    
    except (socket.error, Exception) as e:
        print(f"Erro ao iniciar o servidor: {e}")

def main():
    
    start_server()

if __name__ == "__main__":
    main()
