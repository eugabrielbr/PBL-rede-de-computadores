import socket
import compra
import pickle
from datetime import datetime

def start_client(host='localhost', port=8080):
    # cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # conecta ao servidor
    client_socket.connect((host, port))

    teste = compra.Compra("Gabriel",1,[("sao_paulo","bahia")],datetime.now())
    obj = pickle.dumps(teste)
    
    # envia uma mensagem para o servidor
    print("enviando obejto de compra para o servidor...")
    client_socket.sendall(obj)
    
    # recebe a resposta do servidor
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    
    # fecha a conexão
    client_socket.close()



if __name__ == "__main__":
    start_client()
