import socket

def start_client(host='localhost', port=8080):
    # cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # conecta ao servidor
    client_socket.connect((host, port))
    
    # envia uma mensagem para o servidor
    message = str(input("Digite sua mensagem: "))
    client_socket.send(message.encode())
    
    # recebe a resposta do servidor
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")
    
    # fecha a conexão
    client_socket.close()

if __name__ == "__main__":
    start_client()
