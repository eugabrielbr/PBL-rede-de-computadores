import socket
import compra
import pickle
import os
from datetime import datetime

def start_client(host='172.16.103.226', port=1080):
    # cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # conecta ao servidor
    client_socket.connect((host, port))

    teste = compra.Compra("Gabriel",1,[("sao_paulo","bahia")],datetime.now()) #objeto teste
    obj = pickle.dumps(teste)
    
    # envia uma mensagem para o servidor
    print("enviando obejto de compra para o servidor...")
    client_socket.sendall(obj)
    
    # recebe a resposta do servidor
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")

    
    # fecha a conexão
    client_socket.close()



def limpar_tela():
    """Limpa a tela do terminal para uma visualização mais limpa."""
    os.system('cls' if os.name == 'nt' else 'clear')

def exibir_menu():
    """Exibe o menu principal de forma formatada."""
    limpar_tela()
    print("="*30)
    print("       MENU PRINCIPAL")
    print("="*30)
    print("1. Ver Trechos")
    print("2. Compra")
    print("3. Sair")
    print("="*30)

def ver_trechos():
    """Simula a visualização de trechos."""
    limpar_tela()
    print("="*30)
    print("       VER TRECHOS")
    print("="*30)
    print("Aqui você pode visualizar os trechos disponíveis.")
    input("\nPressione Enter para voltar ao menu principal...")

def compra_menu():
    """Simula o processo de compra."""
    limpar_tela()
    print("="*30)
    print("       COMPRA")
    print("="*30)
    print("Aqui você pode realizar a compra.")
    input("\nPressione Enter para voltar ao menu principal...")

def menu():
    """Função principal que exibe o menu e processa a escolha do usuário."""
    while True:
        exibir_menu()
        
        escolha = input("Escolha uma opção (1/2/3): ")
        
        if escolha == '1':
            ver_trechos()
        elif escolha == '2':
            compra_menu()
        elif escolha == '3':
            limpar_tela()
            print("="*30)
            print("   Saindo do programa...")
            print("="*30)
            break
        else:
            limpar_tela()
            print("="*30)
            print("   Opção inválida! Tente novamente.")
            print("="*30)
            input("\nPressione Enter para continuar...")

    return escolha

def main():
    start_client()
    
    menu()
    
   

if __name__ == "__main__":
    main()