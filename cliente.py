import socket
import os

class Cliente:

    def __init__(self, HOST, PORT):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        
    
    def iniciar_conexao(self):
        self.cliente.connect((self.HOST, self.PORT))
    
    def testar_conexao(self):
        mensagem = "racobaldo".encode()
        self.cliente.send(mensagem)
        data = self.cliente.recv(1024).decode()
        print(data)

    def encerrar_conexao(self):
        print("> Encerrando conexão")
        self.cliente.close()

    # TODO REFORMULAR ISSO
    def criar_usuario(self):
        self.cliente.send("01".encode())
    
    def start(self):
        # PRINTAR TODAS AS OPCOES DO CLIENTE E MANTER DENTRO DE UM LOOP TIPO UM MENU
        self.iniciar_conexao()
        os.system('pause')

        while True:
            print("> Escolha as opções:")
            print("[1] racobaldo")
            print("[2] Criar usuario")
            print("[0] Finalizar Conexão")
            resposta = int(input())

            if resposta == 1:
                self.testar_conexao()
                os.system("pause")
            elif resposta == 2:
                self.criar_usuario()
                os.system("pause")
            elif resposta == 0:
                self.encerrar_conexao()
                break
            else:
                print("> Resposta Inválida!")
                os.system("pause")


if __name__ == '__main__':
    cliente = Cliente('localhost', 6969)
    cliente.start()
