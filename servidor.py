import socket
import pickle

def retornar_trechos():
    trechos_viagem = {
    "São Paulo, SP": {
        "Rio de Janeiro, RJ": {"distancia": 430, "vagas": 5, "preco": 120},
        "Belo Horizonte, MG": {"distancia": 586, "vagas": 8, "preco": 150}
    },
    "Rio de Janeiro, RJ": {
        "São Paulo, SP": {"distancia": 430, "vagas": 5, "preco": 120},
        "Brasília, DF": {"distancia": 1148, "vagas": 0, "preco": 250}
    },
    "Brasília, DF": {
        "Rio de Janeiro, RJ": {"distancia": 1148, "vagas": 0, "preco": 250},
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

def compra(trechos, rotas, id_viagem):
    diminuir_vagas(trechos, rotas[id_viagem])

    # Grafo de trechos de viagem com distâncias, vagas e preços

# Função 1: Diminui o número de vagas em uma rota
def diminuir_vagas(grafo, rota):
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]

        if grafo[cidade_atual][proxima_cidade]["vagas"] > 0:
            # Reduz uma vaga tanto na ida quanto na volta
            grafo[cidade_atual][proxima_cidade]["vagas"] -= 1
            grafo[proxima_cidade][cidade_atual]["vagas"] -= 1
        else:
            print(f"Sem vagas disponíveis entre {cidade_atual} e {proxima_cidade}.")

# Função 2: Calcula o preço total de uma rota
def calcular_preco_total(grafo, rota):
    custo_total = 0
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]
        custo_total += grafo[cidade_atual][proxima_cidade]["preco"]
    return custo_total

# Função 3: Busca todas as possibilidades de rotas de origem a destino
def busca_todos_caminhos(trechos, origem, destino):
    caminhos_encontrados = {}  # Dicionário para armazenar os resultados
    caminho_id = 1  # ID inicial para as rotas

    def dfs(origem, destino, visitado=None, caminho_atual=None, custo_atual=0):
        nonlocal caminho_id
        if visitado is None:
            visitado = set()  # Mantém registro das cidades já visitadas
        if caminho_atual is None:
            caminho_atual = []  # Mantém o caminho atual

        # Adiciona a cidade atual ao caminho
        caminho_atual.append(origem)

        # Se a cidade de origem for o destino, adiciona o caminho ao dicionário de resultados
        if origem == destino:
            caminhos_encontrados[caminho_id] = {
                "caminho": caminho_atual.copy(),  # Clona o caminho atual
                "custo_total": custo_atual
            }
            caminho_id += 1
            caminho_atual.pop()  # Remove a cidade atual do caminho antes de retornar
            return

        # Marca a cidade como visitada
        visitado.add(origem)

        # Verifica todos os trechos disponíveis a partir da cidade de origem
        if origem in trechos:
            for cidade_destino, info_trecho in trechos[origem].items():
                # Verifica se o trecho tem vagas disponíveis e se a cidade não foi visitada ainda
                if info_trecho["vagas"] > 0 and cidade_destino not in visitado:
                    # Atualiza o custo e faz a busca recursiva
                    dfs(
                        cidade_destino, 
                        destino, 
                        visitado, 
                        caminho_atual, 
                        custo_atual + info_trecho["preco"]
                    )

        # Remove a cidade atual do caminho e a desmarca como visitada (backtracking)
        caminho_atual.pop()
        visitado.remove(origem)

    # Inicia a busca em profundidade
    dfs(origem, destino)
    return caminhos_encontrados


def start_server(host='localhost', port=1080):
    
    # criando um socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #AFI_INET - para endereços de redes ipv4
    #SOCK_STREAM - para o protocolo de transmissão de dados TCP
    

    # associando o socket ao endereço da porta 
    socket_server.bind((host, port))
    
    # inicia o servidor para aceitar conexões
    socket_server.listen(0)
    print(f"disponivel em {host} : {port}")
    cont_compra = 0
    while True:        
        # Exemplo de como acessar os atributos das instâncias criadas

        # aceita a conexão
        client_socket, client_address = socket_server.accept()
        print(f"conectado com {client_address}")
        dinheiro = 10
        obj = busca_todos_caminhos(retornar_trechos(), "Salvador, BA", "Fortaleza, CE")
        print(obj)
        data = pickle.dumps(obj)
        # recebe dados do cliente
        client_socket.sendall(data)

        # envia um retorno para o cliente
        response = "objeto recebido com sucesso"
        client_socket.send(response.encode())
        # fecha a conexão
        client_socket.close()

if __name__ == "__main__":
    start_server()
    #teste()
