import socket
import pickle
import os

def start_client(host='localhost', port=1080):
    """Cria e conecta o socket do cliente."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        return client_socket
    except socket.error as e:
        print(f"Erro ao conectar ao servidor: {e}")
        raise

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

def selecionar_origem(opcao):
    """Seleciona a cidade de origem com base na opção escolhida."""
    switch_origem = {
        1: "São Paulo, SP",
        2: "Rio de Janeiro, RJ",
        3: "Brasília, DF",
        4: "Salvador, BA",
        5: "Fortaleza, CE",
        6: "Belo Horizonte, MG",
        7: "Recife, PE",
        8: "Porto Alegre, RS",
        9: "Curitiba, PR",
        10: "Manaus, AM"
    }
    return switch_origem.get(opcao, "Opção inválida")

def print_cidades():
    """Imprime as cidades disponíveis para escolha."""
    print("1. São Paulo, SP")
    print("2. Rio de Janeiro, RJ")
    print("3. Brasília, DF")
    print("4. Salvador, BA")
    print("5. Fortaleza, CE")
    print("6. Belo Horizonte, MG")
    print("7. Recife, PE")
    print("8. Porto Alegre, RS")
    print("9. Curitiba, PR")
    print("10. Manaus, AM")

def compra_menu():
    """Simula o processo de compra."""
    limpar_tela()
    print("="*30)
    print("       COMPRA")
    print("="*30)
    print("Aqui você pode realizar a compra.")
    print("Escolha a origem\n")
    print_cidades()
    
    try:
        opcao = int(input("Escolha uma opção: "))
        cidade1 = selecionar_origem(opcao)
        if cidade1 == "Opção inválida":
            raise ValueError("Opção de origem inválida.")
        
        limpar_tela()

        print("="*30)
        print("       COMPRA")
        print("="*30)
        print("Aqui você pode realizar a compra.")
        print("Escolha o destino\n")
        print_cidades()
        
        opcao1 = int(input("Escolha uma opção: "))
        cidade2 = selecionar_origem(opcao1)
        if cidade2 == "Opção inválida":
            raise ValueError("Opção de destino inválida.")

        return cidade1, cidade2

    except ValueError as ve:
        print(f"Erro na escolha: {ve}")
        return None, None

def menu(client_socket):
    """Função principal que exibe o menu e processa a escolha do usuário."""
    while True:
        exibir_menu()
        
        escolha = input("Escolha uma opção (1/2/3): ")
        
        if escolha == '1':
            ver_trechos()
        elif escolha == '2':
            cidades = compra_menu()
            if cidades == (None, None):
                input("Pressione Enter para voltar ao menu principal...")
                continue

            try:
                obj = pickle.dumps(cidades)
                client_socket.sendall(obj)
                
                # Recebe a resposta do servidor
                data = client_socket.recv(4096)
                if not data:
                    print("Nenhum dado recebido do servidor.")
                    continue

                objeto_recebido = pickle.loads(data)
                print(f"Objeto recebido do servidor: {objeto_recebido}")
            
            except (pickle.PickleError, socket.error) as e:
                print(f"Erro na comunicação: {e}")
            
            input("Pressione Enter para voltar ao menu principal...")
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
            input("Pressione Enter para continuar...")

    client_socket.close()

def main():
    try:
        client_socket = start_client()
        menu(client_socket)
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
