import socket

def start_server(host='localhost', port=8080):
    # criando um socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # associando o socket ao endereço da porta 
    socket_server.bind((host, port))
    
    # inicia o servidor para aceitar conexões
    socket_server.listen(5)
    print(f"ouvindo em {host} : {port}")

    while True:
        # aceita a conexão
        client_socket, client_address = socket_server.accept()
        print(f"conectado com {client_address}")

        # recebe dados do cliente
        data = client_socket.recv(1024).decode()
        print(f"mensagem recebida: {data}")

        # envia um retorno para o cliente
        response = "mensagem recebida com sucesso"
        client_socket.send(response.encode())

        # fecha a conexão
        client_socket.close()

if __name__ == "__main__":
    start_server()
