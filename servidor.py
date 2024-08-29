import socket
import pickle

def start_server(host='172.16.103.226', port=1080):
    # criando um socket
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #AFI_INET - para endereços de redes ipv4
    #SOCK_STREAM - para o protocolo de transmissão de dados TCP


    # associando o socket ao endereço da porta 
    socket_server.bind((host, port))
    
    # inicia o servidor para aceitar conexões
    socket_server.listen(5)
    print(f"disponivel em {host} : {port}")
    cont_compra = 0
    while True:
        # aceita a conexão
        client_socket, client_address = socket_server.accept()
        print(f"conectado com {client_address}")

        # recebe dados do cliente
        data = client_socket.recv(4096)
        objeto_recebido = pickle.loads(data)

        # envia um retorno para o cliente
        response = "objeto recebido com sucesso"
        client_socket.send(response.encode())

        print(f"\nDADOS DA COMPRA: {cont_compra}\n")
        print(f"nome: {objeto_recebido.usuario}\nid: {objeto_recebido.id_usuario}\ntrecho: {objeto_recebido.trecho}\ndata: {objeto_recebido.data}")


        # fecha a conexão
        client_socket.close()

if __name__ == "__main__":
    start_server()
