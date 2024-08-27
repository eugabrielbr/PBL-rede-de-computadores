import socket

def start_server(host='localhost', port=8080):
    # criando um socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # associando o socket ao endereço da porta 
    socket_server.bind((host, port))
    
    # Inicia o servidor para aceitar conexões
    socket_server.listen(5)
    print(f"ouvindo em {host} : {port}")

    while True:
        # Aceita uma conexão
        client_socket, client_address = socket_server.accept()
        print(f"conectado com {client_address}")

        # Recebe dados do cliente
        data = client_socket.recv(1024).decode()
        print(f"mensagem recebida: {data}")

        # Envia uma resposta para o cliente
        response = "mensagem recebida com sucesso"
        client_socket.send(response.encode())

        # Fecha a conexão com o cliente
        client_socket.close()

if __name__ == "__main__":
    start_server()
