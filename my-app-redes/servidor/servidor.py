"""
Arquivo do servidor, utilizado para hospedar os dados de clientes e trechos
fazendo com que seja possível todos os usuários conectados ao servidor conectem
e acessem os dados um de cada vez para realizar consultar de trechos, comprar passagens
e ver passagens compradas.
"""

import socket
import pickle
from pathlib import Path
import json
import threading
import time

caminho_arquivo = Path(__file__).parent / "trechos_viagem.json" # nome do JSON utilizado para salvar no arquivo.


class Cliente:
    """
    Classe cliente, utilizada para identificar a pessoa que está realizando compra, 
    foi criada com o intuito de possibilitar o acesso à suas próprias compras
    mesmo em um IP diferente.
    """
    def __init__(self, cpf, trechos):
        self.cpf = cpf
        self.trechos = trechos
    def to_dict(self):
        """
        Transforma a classe cliente em um dicionário contendo cpf e trechos como chave, essa função
        foi feita para ser possível salvar os objetos da classe no arquivo JSON
        """
        return {
            'cpf': self.cpf,
            'trechos': self.trechos
        }


def salvar_json(dados, caminho_arquivo):
    """
    Função utilizada para salvar os dados do clientes 
    e os trechos contidos dentro do sistema, o salvamento é feito no JSON.
    """
    with open(caminho_arquivo, 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False)

def carregar_json(caminho_arquivo):
    """
    Função utilizada para carregar os dados do clientes e os trechos contidos dentro do JSON, o carregamento é feito a partir de um JSON.
    """
    with open(caminho_arquivo, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def salvar_trecho(trechos):
    """
    Essa função carrega os dados JSON do arquivo para que seja possível pegar a versão mais recente tanto dos trechos quantos dos clientes, para salvar uma nova versão dos trechos
    no JSON do sistema.
    """
    dados = carregar_json(caminho_arquivo)
    dados["trechos"] = trechos
    salvar_json(dados, caminho_arquivo)

def salvar_clientes(clientes):
    """
    Essa função carrega os dados JSON do arquivo para que
    seja possível pegar a versão mais recente tanto dos
    trechos quantos dos clientes, para salvar uma nova versão dos clientes
    no JSON do sistema, aqui os clientes utilizam a função 
    .todict para virar um dicionário, assim a serialização é possível.
    """
    dados = carregar_json(caminho_arquivo)
    print(f"tamanho {len(clientes)} {clientes}")
    dados["clientes"] = [cliente.to_dict() for cliente in clientes]
    salvar_json(dados, caminho_arquivo)

def carregar_clientes():
    """
    Carrega os clientes do arquivo JSON para o programa em execução, aqui,
    a função transforma os dicionários de clientes em objeto da classe Cliente,
    para que possa ser usado no programa em execução
    """
    dados = carregar_json(caminho_arquivo)
    if len(dados["clientes"]) != 0:
        return [Cliente(**cliente_json) for cliente_json in dados["clientes"]]
    else:
        return []

def carregar_trechos():
    """
    Carrega os trechos do arquivo JSON para o programa em execução.
    """
    dados = carregar_json(caminho_arquivo)
    return dados["trechos"].copy()

def trechos_cliente(cliente_cpf):
    """
    Essa função busca os trechos comprados de um cliente a partir do CPF passado como paramêtro
    """
    clientes = carregar_clientes()
    for cliente in clientes:
        if cliente_cpf == cliente.cpf:
            return cliente.trechos

def editar_trecho(caminho, cliente_conectado, lock):
    """
    Essa função é utilizada para efetuar a compra de um trecho para um usuário, basicamente, 
    a função recebe um trecho e verifica se nesse trecho tem vagas
    para que seja possível realizar a compra do trecho para o usuário,
    a verificação é feita utilizando o mutex, para evitar que dois clientes acessem e salvem
    informações divergentes do sistema, quando o trecho tem vagas para o cliente, a compra é feita, 
    caso não, a compra é recusada e o cliente não consegue comprar.
    """
    with lock:
        trechos_viagem = carregar_trechos()
        trecho = caminho["caminho"].copy()
        print(caminho["caminho"])
        print(trechos_viagem[trecho[0]][trecho[1]]["vagas"])
        while len(trecho) > 1:
            if trechos_viagem[trecho[0]][trecho[1]]["vagas"] > 0:
                trechos_viagem[trecho[0]][trecho[1]]["vagas"] -= 1
                print(trechos_viagem[trecho[0]][trecho[1]]["vagas"])
                trecho.pop(0)
            elif trechos_viagem[trecho[0]][trecho[1]]["vagas"] < 1:
                return False
        salvar_trecho(trechos_viagem)
        print(caminho["caminho"])
        adicionar_trecho_cliente(cliente_conectado, caminho["caminho"])
        return True

def adicionar_cliente_arquivo(cliente):
    """
    Aqui um cliente é salvo no arquivo pela primeira vez após o login
    caso não tenha cadastro, caso já haja cadastro, não acontece nada.
    """
    clientes = carregar_clientes()
    adicionado = False
    for obj in clientes:
        if obj.cpf == cliente.cpf:
            index = clientes.index(obj)
            clientes[index] = cliente
            adicionado = True
    if not adicionado:
        clientes.append(cliente)
    salvar_clientes(clientes)
    return True

def encontrar_cliente(cliente):
    """
    Função utilizada para encontrar um cliente no arquivo do sistema, caso encontre, 
    retorna o cliente, caso não, retorna None
    """
    clientes = carregar_clientes()
    for obj in clientes:
        if obj.cpf == cliente.cpf:
            return obj
    return None

def inicializar_clientes():
    """Inicializa a lista de clientes conectados"""
    return []

def adicionar_cliente_conectado(cliente, lista_clientes):
    """Adiciona um cliente à lista de clientes conectados"""
    lista_clientes.append(cliente)

def remover_cliente_conectado(cliente, lista_clientes):
    """Remove um cliente à lista de clientes conectados"""
    lista_clientes.remove(cliente)

def listar_clientes(lista_clientes, lock):
    """Retorna a lista de clientes conectados"""
    with lock:  # Garante que apenas uma thread por vez entre aqui
        return lista_clientes.copy()  # Use copy() para evitar problemas de leitura simultânea

def adicionar_trecho_cliente(cpf, trecho):
    """
    Função que adiciona um trecho comprado para o cpf do cliente.
    """
    clientes = carregar_clientes()
    i = 1
    for obj in clientes:
        if obj.cpf == cpf:
            while(str(i) in obj.trechos.keys()):
                i = i + 1
                print(f"i: {i}")
            obj.trechos[i] = [" -> ".join(trecho)]
            salvar_clientes(clientes)
            return True
    return False




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

# o timeout do servidor serve somente para garantir q o cliente se desconecte em envio muito demorado de pacotes, evitando sobrecarga
# por isso seu timer é de 100s
def start_server(host=socket.gethostbyname(socket.gethostname()), port=4000, timeout = 120):
    """Inicia o servidor para aceitar conexões de clientes e processar dados."""
    lock = threading.Lock()
    clientes_conectados = inicializar_clientes()
    try:
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.bind((host, port))
        socket_server.listen(5)
        print(f"Disponível em {host}:{port}")

        # Loop para aceitar conexões de clientes
        while True:
            client_socket, client_address = socket_server.accept()
            client_socket.settimeout(timeout)
            thread = threading.Thread(target=thread_cliente, args=(client_socket, client_address, clientes_conectados, lock,timeout))
            thread.start()
    except (socket.error, Exception) as e:
        print(f"Erro ao iniciar o servidor: {e}")


def thread_cliente(client_socket, client_address, clientes_conectados, lock,timeout):
    #client_socket, client_address = socket_server.accept()
    """Função que lida com cada cliente em uma nova thread."""
    cliente_conectado = checar_conexao(client_socket, clientes_conectados, lock)
    print(f"Conectado com {client_address}")
    with lock:
        dados = carregar_json(caminho_arquivo)
        print(dados)
        trechos_viagem = carregar_trechos()
    last_activity = time.time()
    # Recebendo dados de login:
    try:
        # Inicia o loop de comunicação com o cliente
        while True:
            if cliente_conectado is None:
                break

            if time.time() - last_activity > timeout:
                client_socket.sendall(pickle.dumps("timeout"))
                break
            try:
                data = client_socket.recv(4096)
                if not data:
                    break

                obj = pickle.loads(data)

                if obj == "trechos":
                    new_obj = trechos_viagem # Servidor envia os trechos para o cliente conseguir visualizar.
                elif obj[0] == "compra":
                    compra = editar_trecho(obj[1], cliente_conectado, lock) # Servidor recebe o trajeto que o cliente escolheu e realiza a compra para o cpf do cliente.
                    if compra: # se a compra foi um sucesso, o obj a ser enviado será true indicando a compra
                        new_obj = True
                    else: # se a compra falhou, obj à ser enviado será um False indicando que não houve a compra.
                        new_obj = False
                elif obj[0] == "viagem": # Recebe o origem e o destino e busca todas possibilidades de trajeto
                    cidade1, cidade2 = obj[1]
                    new_obj = busca_possibilidades(trechos_viagem, cidade1, cidade2)
                elif obj == "trechos_cliente": # Retorna os trechos comprados de um cliente.
                    new_obj = trechos_cliente(cliente_conectado)
                elif obj == "saida" or obj == "timeout": # Caso o cliente saia ou tome timeout.
                    break
                data_send = pickle.dumps(new_obj)
                client_socket.sendall(data_send)
                last_activity = time.time()

            except (pickle.PickleError, socket.error) as e:
                print(f"Erro na comunicação: {e}")
                break
            with lock:
                dados = carregar_json(caminho_arquivo)
            trechos_viagem = carregar_trechos()
        if cliente_conectado is not None: # Ao cliente ser desconectado, retira ele da lista de clientes conectados.
            for cliente_iterator in clientes_conectados:
                if cliente_conectado == cliente_iterator.cpf:
                    cliente_copia = cliente_iterator
                    break
            print(f"Cliente de CPF {cliente_copia.cpf} foi desconectado.")
            with lock:
                remover_cliente_conectado(cliente_copia, clientes_conectados)
            client_socket.close()



    except (pickle.PickleError, socket.error) as e:
        print(f"Erro na comunicação com o cliente: {e}")

def checar_conexao(client_socket, clientes_conectados, lock):
    """
    Função cadastra um cliente no servidor caso não tenha sido cadastro e 
    impede duplas conexões de um mesmo CPF no servidor.
    """
    # Recebendo dados de login:
    try:
        while True:
            clientes = carregar_clientes()
            data_login = client_socket.recv(4096)
            obj_login = pickle.loads(data_login)
            # Processo de consulta de cliente
            if obj_login[0] == "consulta":
                dados = carregar_json(caminho_arquivo)
                cliente_consultado = None
                if len(dados["clientes"]) != 0:
                    for cliente in clientes:
                        if cliente.cpf == obj_login[1]:
                            cliente_consultado = cliente
                            break
                if cliente_consultado is None:
                    cliente_consultado = Cliente(obj_login[1], {})
                data_send = pickle.dumps(cliente_consultado)
                client_socket.sendall(data_send)
            with lock:
                # Recebendo novo login
                data_login = client_socket.recv(4096)
                obj_login = pickle.loads(data_login)

                # Verifica se o cliente já está conectado
                liberado = True
                for obj in clientes_conectados:
                    if obj_login.cpf == obj.cpf:
                        client_socket.sendall(pickle.dumps(False))
                        print(f"conexao com {obj_login.cpf} negada. Motivo: cliente já está conectado")
                        liberado = False
                        break
                if liberado:
                    client_socket.sendall(pickle.dumps(True))
                    print(f"conexao com o cliente {obj_login.cpf} estabelecida")
                    adicionar_cliente_conectado(obj_login, clientes_conectados)
                    adicionar_cliente_arquivo(obj_login)
                    return obj_login.cpf
    except (pickle.PickleError, socket.error) as e:
        print(f"Erro na comunicação com o cliente: {e}")


def main():
    """Inicia o servidor"""
    start_server()

if __name__ == "__main__":
    main()
