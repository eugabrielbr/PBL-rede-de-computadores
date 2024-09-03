import socket
import compra
import pickle
import os
from datetime import datetime

def start_client(host='localhost', port=1080):
    # cria um socket TCP
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # conecta ao servidor
    client_socket.connect((host, port))
    cidades_com_aeroporto = [
        "São Paulo, SP",
        "Rio de Janeiro, RJ",
        "Brasília, DF",
        "Salvador, BA",
        "Fortaleza, CE",
        "Belo Horizonte, MG",
        "Recife, PE",
        "Porto Alegre, RS",
        "Curitiba, PR",
        "Manaus, AM",
        "Belém, PA",
        "Goiânia, GO",
        "Vitória, ES",
        "Florianópolis, SC",
        "Maceió, AL",
        "Natal, RN",
        "São Luís, MA",
        "Cuiabá, MT",
        "Aracaju, SE",
        "Campo Grande, MS"
    ]

    # Lista para armazenar as instâncias da classe Cidade
    cidades_objetos = []

    # Loop para criar instâncias da classe Cidade e adicionar à lista
    for i, cidade_estado in enumerate(cidades_com_aeroporto):
        nome, estado = cidade_estado.split(", ")
        cidade_itr = compra.Cidade(nome, estado, str(i + 1))  # Atribuindo o ID como um índice sequencial
        cidades_objetos.append(cidade_itr)

    # Exemplo de como acessar os atributos das instâncias criadas

    print(f"ID: {cidade_itr.id}, Nome: {cidade_itr.nome}, Estado: {cidade_itr.estado}")
    client_socket.send(pickle.dumps(cidades_objetos))
    response = client_socket.recv(1024).decode()
    print(f"Server response: {response}")
    # envia uma mensagem para o servidor
    print("enviando obejto de compra para o servidor...")    # recebe a resposta do servidor

    
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
    
    #menu()
    
   

if __name__ == "__main__":
    main()