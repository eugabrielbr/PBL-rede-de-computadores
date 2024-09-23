import socket
import pickle
import os
import sys 


class Cliente:
    def __init__(self, cpf, trechos):
        self.cpf = cpf
        self.trechos = trechos
    
    def to_dict(self):
        return {
            'cpf': self.cpf,
            'trechos': self.trechos
        }

def start_client(host='localhost', port=8080):
    """Cria e conecta o socket do cliente."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(30)
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
    print("1. Ver Trechos disponíveis")
    print("2. Trechos comprados")
    print("3. Compra")
    print("4. Sair")

    print("="*30)

def ver_trechos():
    """Simula a visualização de trechos."""
    limpar_tela()
    print("="*30)
    print("       VER TRECHOS")
    print("="*30)
    print("Aqui você pode visualizar os trechos disponíveis.")

def selecionar_origem(opcao):
    """Seleciona a cidade de origem com base na opção escolhida."""
    switch_origem = {
        1: "São Paulo-SP",
        2: "Rio de Janeiro-RJ",
        3: "Brasília-DF",
        4: "Salvador-BA",
        5: "Fortaleza-CE",
        6: "Belo Horizonte-MG",
        7: "Recife-PE",
        8: "Porto Alegre-RS",
        9: "Curitiba-PR",
        10: "Manaus-AM"
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

    except ValueError:
        print("Opção inválida, utilize os números de 1-10")
        return None, None

def menu(client_socket):
    """Função principal que exibe o menu e processa a escolha do usuário."""
    data_ver = login(client_socket)
   

    if data_ver == True:
        
        while True:
            
            exibir_menu()
            
            
            escolha = input("Escolha uma opção (1/2/3/4): ")
            
            if escolha == '1':
                ver_trechos()
                try:
                    obj = pickle.dumps("trechos")
                    client_socket.sendall(obj)
                    
                    # Recebe a resposta do servidor
                    data = client_socket.recv(4096)
                    
                    if not data:
                        print("Nenhum dado recebido do servidor.")
                        continue

                    objeto_recebido = pickle.loads(data)
                    # print(f"Objeto recebido do servidor: {objeto_recebido}")
                    i = 1
                    for obj in objeto_recebido.keys():
                        print(f"Origem {i}: {format(obj)}")
                        i += 1
                        j = 1
                        print()
                        for obj_ex in objeto_recebido[obj]:
                            print(f"[Trecho {j}: {obj_ex}] | [Distância: {objeto_recebido[obj][obj_ex]['distancia']}km] | [Vagas: {objeto_recebido[obj][obj_ex]['vagas']}] | [Valor: R${objeto_recebido[obj][obj_ex]['preco']}]")
                            j += 1
                        print()

                except (pickle.PickleError, socket.error) as e:
                    print(f"Erro na comunicação: {e}")
                
                input("Pressione Enter para voltar ao menu principal...")
            
            elif escolha == '2':
                try:
                    obj = pickle.dumps("trechos_cliente")
                    client_socket.sendall(obj)
                    # Recebe a resposta do servidor
                    data = client_socket.recv(4096)
                    if not data:
                        print("Nenhum dado recebido do servidor.")
                        continue
                    objeto_recebido = pickle.loads(data)
                    if(len(objeto_recebido) < 1):
                        print("Você não tem trechos comprados.")
                    else:
                        for n_trecho, trecho in objeto_recebido.items():
                            print(f"{n_trecho}: {trecho}")
                except (pickle.PickleError, socket.error) as e:
                    print(f"Erro na comunicação: {e}")
                
                input("Pressione Enter para voltar ao menu principal...")

            elif escolha == '3':
                cidades = compra_menu()
                if cidades == (None, None):
                    input("Pressione Enter para voltar ao menu principal...")
                    continue

                try:
                    obj = pickle.dumps(("viagem",cidades))
                    client_socket.sendall(obj)
                    
                    # Recebe a resposta do servidor
                    data = client_socket.recv(4096)
                    
                    if not data:
                        print("Nenhum dado recebido do servidor.")
                        continue

                    objeto_recebido = pickle.loads(data)
                    for caminho in objeto_recebido:
                        stringteste = " -> ".join(objeto_recebido[caminho]['caminho'])
                        print(f"Trajeto {caminho}:\n{stringteste}\nValor: R${objeto_recebido[caminho]['preco_total']}")
                        print()
                    if not objeto_recebido:
                        print("Não há trechos disponíveis para realizar essa viagem.")
                    else:
                        condicao = True
                        condicao2 = False
                        while condicao:
                            print()
                            escolha_trecho = input("Escolha o trecho desejado(para desistir digite 'cancelar'): ")
                            if escolha_trecho == "cancelar":
                                break
                            if escolha_trecho.isnumeric() and 1 <= int(escolha_trecho) <= 10:
                                condicao = False
                                condicao2 = True
                        if condicao2:
                            obj1 = pickle.dumps(("compra", objeto_recebido[int(escolha_trecho)]))
                            client_socket.sendall(obj1)
                            data = client_socket.recv(4096)
                        if not data:
                            print("Nenhum dado recebido do servidor.")
                            continue
                        objeto_recebido = pickle.loads(data)
                        if(objeto_recebido):
                            print("Compra realizada com sucesso!")
                        else:
                            print("Houve um erro no momento da sua compra, tente novamente.")

                except (pickle.PickleError, socket.error) as e:
                    print(f"Erro na comunicação: {e}")
                
                input("Pressione Enter para voltar ao menu principal...")
            elif escolha == '4':
                obj1 = pickle.dumps(("saida"))
                client_socket.sendall(obj1)
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
    else:
        print("Cliente já está logado, tente novamente mais tarde")

    client_socket.close()

def login(client_socket):
    valido = True
    while(valido):
        
        if len(sys.argv) > 1:
            cpf = sys.argv[1]
        else: 
            cpf = str(input("Insira CPF: "))
            
        obj = pickle.dumps(("consulta", cpf))
        client_socket.sendall(obj)
        data = client_socket.recv(4096)
        cliente_recebido = pickle.loads(data)
        print(f"{cliente_recebido} -> dado recebido do servidor.")
        # Verificando cliente logado
        try:
            obj_cliente = pickle.dumps(cliente_recebido)
            client_socket.sendall(obj_cliente)
        except:
            pass

        data_ver = client_socket.recv(4096)
        data_ver = pickle.loads(data_ver)
        if(data_ver is True):
            valido = False
        else:
            print("CPF já está logado no servidor")

    return data_ver

def main():
    try:
        client_socket = start_client()
        menu(client_socket)
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
