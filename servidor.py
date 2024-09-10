import socket
import pickle

def retornar_trechos():
    """Retorna o dicionário de trechos de viagem."""
    trechos_viagem = {
        "São Paulo, SP": {
            "Rio de Janeiro, RJ": {"distancia": 430, "vagas": 1, "preco": 120},
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
    return trechos_viagem

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
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind((host, port))
        socket_server.listen(5)
        print(f"Disponível em {host} : {port}")

        while True:
            client_socket, client_address = socket_server.accept()
            print(f"Conectado com {client_address}")

            try:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    
                    obj = pickle.loads(data)
                    print(f"Dados recebidos: {obj}")
                    if(obj == "trechos"):
                        new_obj = retornar_trechos()
                    else:
                        cidade1, cidade2 = obj
                        new_obj = busca_possibilidades(retornar_trechos(), cidade1, cidade2)
                    data_send = pickle.dumps(new_obj)
                    client_socket.sendall(data_send)

            except (pickle.PickleError, socket.error) as e:
                print(f"Erro na comunicação: {e}")
            finally:
                client_socket.close()

    except (socket.error, Exception) as e:
        print(f"Erro ao iniciar o servidor: {e}")

if __name__ == "__main__":
    start_server()
