from datetime import datetime
import pickle

class Compra:

    def __init__(self,usuario: str, id_usuario: int, trecho: list, data: datetime):

        self.usuario = usuario
        self.id_usuario = id_usuario
        self.trecho = trecho
        self.data = data
    
    def definir_trecho(self, origem:int,destino:int) -> tuple:
        
        origem_str = ''
        destino_str = ''

        if origem == 1:
            origem_str = "sao_paulo"
        elif origem == 2:
            origem_str = "bahia"
        elif origem == 3:
            origem_str = "minas"

        if destino == 1:
            destino_str = "sao_paulo"
        elif destino == 2:
            destino_str = "bahia"
        elif destino == 3:
            destino_str = "minas"

        return (origem_str,destino_str)

class Cidade:

   def __init__(self,nome: str,estado:str,id:str):
       self.nome = nome
       self.estado = estado
       self.id = id
    
class Trecho:

    def __init__(self,origem:Cidade,destino:Cidade,id:str):

        self.origem = origem
        self.destino = destino 
        self.id = id




def main():

    ''

if __name__ == "__main__":
    main()