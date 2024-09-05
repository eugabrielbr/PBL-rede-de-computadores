import socket
import pickle


def compra(trechos, rotas, id_viagem):
    diminuir_vagas(trechos, rotas[id_viagem])

def diminuir_vagas(trechos, rota):
    # Percorre o caminho (rota), de uma cidade para a próxima
    for i in range(len(rota) - 1):
        cidade_atual = rota[i]
        proxima_cidade = rota[i + 1]

        # Verifica se existe o trecho no grafo e se há vagas
        if trechos[cidade_atual][proxima_cidade]["vagas"] > 0:
            # Diminui o número de vagas em 1
            trechos[cidade_atual][proxima_cidade]["vagas"] -= 1
            # Como o grafo é bidirecional, diminui o número de vagas no caminho inverso também
            trechos[proxima_cidade][cidade_atual]["vagas"] -= 1
        else:
            print(f"Sem vagas disponíveis entre {cidade_atual} e {proxima_cidade}.")

def mostrar_possibilidades(origem, destino):
    rotas = busca_possibilidades(origem, destino)
    for id_rota, rota in rotas.items():
        print(f"Rota {id_rota}: {' -> '.join(rota)}")

def busca_possibilidades(origem, destino):
    trechos = definir_rotas()
    rotas = {}  # Dicionário para armazenar as rotas com ID
    id_rota = 1  # ID inicial para as rotas

    # Função para realizar a busca em profundidade
    def dfs(cidade_atual, caminho):
        nonlocal id_rota
        caminho.append(cidade_atual)

        # Se chegamos ao destino, armazena o caminho
        if cidade_atual == destino:
            rotas[id_rota] = caminho
            id_rota += 1
        else:
            # Para cada vizinho da cidade atual
            for vizinho, info in trechos[cidade_atual].items():
                # Se o número de vagas for maior que zero e o vizinho não tiver sido visitado
                if info["vagas"] > 0 and vizinho not in caminho:
                    dfs(vizinho, caminho[:])  # Chamada recursiva com uma cópia do caminho

    # Inicia a busca a partir da cidade de origem
    dfs(origem, [])

    return rotas  # Retorna o dicionário de rotas

def definir_rotas() -> dict:
    trechos_viagem = {
        "São Paulo - SP": {
            "Rio de Janeiro - RJ": {"distancia": 430, "vagas": 5},
            "Belo Horizonte - MG": {"distancia": 586, "vagas": 8}
        },
        "Rio de Janeiro - RJ": {
            "São Paulo - SP": {"distancia": 430, "vagas": 5},
            "Brasília - DF": {"distancia": 1148, "vagas": 3}
        },
        "Brasília - DF": {
            "Rio de Janeiro - RJ": {"distancia": 1148, "vagas": 3},
            "Salvador - BA": {"distancia": 1440, "vagas": 6}
        },
        "Salvador - BA": {
            "Brasília - DF": {"distancia": 1440, "vagas": 6},
            "Fortaleza - CE": {"distancia": 1023, "vagas": 4}
        },
        "Fortaleza - CE": {
            "Salvador - BA": {"distancia": 1023, "vagas": 4},
            "Recife - PE": {"distancia": 800, "vagas": 10}
        },
        "Belo Horizonte - MG": {
            "São Paulo - SP": {"distancia": 586, "vagas": 8},
            "Porto Alegre - RS": {"distancia": 1712, "vagas": 7}
        },
        "Recife - PE": {
            "Fortaleza - CE": {"distancia": 800, "vagas": 10},
            "Manaus - AM": {"distancia": 2714, "vagas": 2}
        },
        "Porto Alegre - RS": {
            "Belo Horizonte - MG": {"distancia": 1712, "vagas": 7},
            "Curitiba - PR": {"distancia": 711, "vagas": 9}
        },
        "Curitiba - PR": {
            "Porto Alegre - RS": {"distancia": 711, "vagas": 9},
            "São Paulo - SP": {"distancia": 408, "vagas": 5}
        },
        "Manaus - AM": {
            "Recife - PE": {"distancia": 2714, "vagas": 2},
            "Brasília - DF": {"distancia": 1930, "vagas": 6}
        }
    }    
    return trechos_viagem



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
        client_socket.send(pickle.dumps(cidades_objetos))
        # aceita a conexão
        client_socket, client_address = socket_server.accept()
        print(f"conectado com {client_address}")

        # recebe dados do cliente
        data = client_socket.recv(4096)
        objeto_recebido = pickle.loads(data)

        # envia um retorno para o cliente
        response = "objeto recebido com sucesso"
        client_socket.send(response.encode())
        for obj in objeto_recebido:
            print(f"nome: {obj.nome}\nid: {obj.id}\nestado: {obj.estado}")

        
        # fecha a conexão
        client_socket.close()

if __name__ == "__main__":
    start_server()
