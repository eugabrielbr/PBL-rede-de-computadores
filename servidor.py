import socket
import pickle
from cliente import Cliente
import json

caminho_arquivo = "trechos_viagem.json"


def salvar_json(dados, caminho_arquivo):
    with open(caminho_arquivo, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False)

# Função para carregar o dicionário de um arquivo JSON
def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def salvar_trecho(trechos):
    dados = carregar_json(caminho_arquivo)
    dados["trechos"] = trechos
    salvar_json(dados, caminho_arquivo)

def salvar_clientes(clientes):
    dados = carregar_json(caminho_arquivo)
    dados["clientes"] = clientes
    salvar_json(dados, caminho_arquivo)

def carregar_clientes():
    dados = carregar_json(caminho_arquivo)
    return dados["clientes"]

def editar_trecho(caminho, trechos_viagem):
    trecho = caminho["caminho"]
    print(trechos_viagem[trecho[0]][trecho[1]]["vagas"])
    while len(trecho) > 1:
        if trechos_viagem[trecho[0]][trecho[1]]["vagas"] > 0:
            trechos_viagem[trecho[0]][trecho[1]]["vagas"] -= 1
            print(trechos_viagem[trecho[0]][trecho[1]]["vagas"])
            trecho.pop(0)
        elif trechos_viagem[trecho[0]][trecho[1]]["vagas"] < 1:
            return False
    salvar_trecho(trechos_viagem)
    return True

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
    clientes_conectados = []
    dados = carregar_json(caminho_arquivo)
    print(dados)
    clientes = dados["clientes"]
    trechos_viagem = dados["trechos"]
    salvar_json({"clientes": clientes, "trechos": trechos_viagem}, caminho_arquivo)
    
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
                clientes = carregar_clientes
                data_login = client_socket.recv(4096)
                obj_login = pickle.loads(data_login)
                if obj_login[0] == "consulta":
                    dados = carregar_json(caminho_arquivo)
                    cliente_consultado = None
                    if len(dados["clientes"]) != 0:
                        for cliente in clientes:
                            if(cliente.cpf == obj_login[1]):
                                cliente_consultado = cliente
                                break
                    if(cliente_consultado is None):
                        cliente_consultado = Cliente(obj_login[1], [])
                    data_send = pickle.dumps(cliente_consultado)
                    client_socket.sendall(data_send)
                    print(f"Foi:{cliente_consultado}")
                data_login = client_socket.recv(4096)
                obj_login = pickle.loads(data_login)
                # Se o cliente já está conectado em outro IP ou no mesmo, ele é desconectado
                liberado = True
                for obj in clientes_conectados:
                    if (obj_login.cpf == obj.cpf):
                        client_socket.sendall(pickle.dumps(False))
                        print(f"conexao com {obj_login.cpf} negada. Motivo: cliente já está conectado")
                        client_socket.close()
                        block = False
                        liberado = False
                        break
                if(liberado):
                    client_socket.sendall(pickle.dumps(True))
                    print(f"conexao com o cliente {obj_login.cpf} estabelecida")
                    cliente_conectado = obj_login
                    clientes_conectados.append(cliente_conectado)
                    block = True
                    #salvar_clientes(clientes)

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
                            new_obj = trechos_viagem
                        elif obj[0] == "compra":
                            compra = editar_trecho(obj[1], trechos_viagem)
                            if compra:
                                cliente_conectado.trechos.append(obj[1])
                        elif obj[0] == "viagem":
                            cidade1, cidade2 = obj[1]
                            new_obj = busca_possibilidades(trechos_viagem, cidade1, cidade2)

                        data_send = pickle.dumps(new_obj)
                        client_socket.sendall(data_send)

                    except (pickle.PickleError, socket.error) as e:
                        print(f"Erro na comunicação: {e}")
                        break

                    dados = carregar_json(caminho_arquivo)
                    clientes = dados["clientes"]
                    trechos_viagem = dados["trechos"]

                print(f"antes{clientes_conectados}")
                #if cliente_conectado in clientes_conectados:
                for cliente_iterator in clientes_conectados:
                    if (cliente_conectado.cpf == cliente_iterator.cpf):
                        client_socket.close()
                        cliente_copia = cliente_iterator
                        break
                clientes_conectados.remove(cliente_copia)
                print(f"depois{clientes_conectados}")


    except (socket.error, Exception) as e:
        print(f"Erro ao iniciar o servidor: {e}")

def main():
    
    start_server()

if __name__ == "__main__":
    main()
