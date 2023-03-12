import socket
import sqlite3
import threading

class Servidor:
    def __init__(self, HOST, PORT):
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.servidor.bind((self.HOST, self.PORT))      # Informando o local e endereço do servidor
        self.iniciar_banco()
        self.listen(10)                               # Numero total de acessos simultâneos (o servidor recusará caso exceda)
    
    def listen(self, num_conexoes):
        print('> Aguardando conexões')
        self.servidor.listen(num_conexoes)
    
    def gerenciar_cliente(self, conexao, endereco):
        print(f"> Conexão encontrada! -> {endereco}")
        conexao.send("> Conexão feita com sucesso!".encode())

        while True:
            try:
                data = conexao.recv(1024).decode()
                if not data:
                    break

                if data == 'racobaldo':
                    data += ' + Gabi + Carro'
                    conexao.send(data.encode())
                
                # MINHA SUGESTAO PARA TRATAR DAS REQUISIÇÕES DO USUÁRIO
                if data[0]+data[1] == "01":
                    self.criar_usuario()

            except ConnectionResetError:
                break

        conexao.close()
        print(f"> Conexão encerrada: {endereco}")


    # Metodo *G E N E R I C O* para iniciar um banco *G E N E R I C O*
    def iniciar_banco(self):

        self.banco = sqlite3.connect('usuarios.db')

        # Cria uma tabela para armazenar os usuários (se ela não existir)
        self.banco.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             NOME TEXT NOT NULL,
             EMAIL TEXT NOT NULL,
             SENHA TEXT NOT NULL);''')

    def salvar_banco(self):
        self.banco.commit()

    def encerrar_conexao_banco(self):
        self.banco.close()

    def criar_usuario(self):
        pass

    def start(self):
        while True:
            conexao, endereco = self.servidor.accept()
            thread = threading.Thread(target=self.gerenciar_cliente, args=(conexao, endereco))
            thread.start()

if __name__ == '__main__':
    server = Servidor('localhost', 6969)
    server.start()