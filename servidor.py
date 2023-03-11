import socket
import sqlite3
import threading

class Servidor:
    def __init__(self, HOST, PORT):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.servidor.bind((self.HOST, self.PORT))
    
    def listen(self, num_conexoes):
        print('aguardando conexoes')
        self.servidor.listen(num_conexoes)
    
    def gerenciar_cliente(self, mensagem):
        pass

    def start(self):
        #TODO COLOCAR THREADs
        conexao, endereco = self.servidor.accept()

        while True:
            data = conexao.recv(1024).decode()
            if not data:
                break

            #TODO TRATAR TODAS AS REQUISIÇÕES
            data += ' + Gabi + Carro'
            conexao.send(data.encode())


server = Servidor('localhost', 6969)
server.listen(1)
server.start()