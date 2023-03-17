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

        while True:
            try:
                data = conexao.recv(1024).decode()
                if not data:
                    break

                if data == 'teste':
                    data += '> Conexão existe!'
                    conexao.send(data.encode())

                # acessando conta
                if data[0]+data[1] == "01":
                    data = data.split(';')
                    retorno = self.acessar_conta(data[1], data[2])
                    if retorno[0] == 200:
                        mensagem = '200;' + str(retorno[1]) + ';' + str(retorno[2]) + ';' + str(retorno[3])
                        conexao.send(mensagem.encode())
                    else:
                        conexao.send("400;Algo deu errado :(".encode())

                # criando nova conta
                if data[0]+data[1] == "02":
                    data = data.split(';')
                    retorno = self.criar_usuario(data[1], data[2], data[3], data[4])
                    if retorno == 200:
                        conexao.send("Usuário criado com sucesso!".encode())
                    else:
                        conexao.send("Algo deu errado :(".encode())

                # acessando saldo da conta
                if data[0]+data[1] == "03":
                    data = data.split(';')
                    retorno = self.consultar_saldo(data[1])
                    if retorno[0] == 200:
                        mensagem = '200;' + str(retorno[1])
                        conexao.send(mensagem.encode())
                    else:
                        conexao.send("400;Algo deu errado :(".encode())

                # creditando saldo na conta
                if data[0]+data[1] == "04":
                    data = data.split(';')
                    retorno = self.creditar_conta(data[1], float(data[2]))
                    if retorno[0] == 200:
                        mensagem = '200'
                        conexao.send(mensagem.encode())
                    else:
                        conexao.send("400;Algo deu errado :(".encode())

                # creditando saldo na conta
                if data[0]+data[1] == "05":
                    data = data.split(';')
                    retorno = self.debitar_conta(data[1], float(data[2]))
                    if retorno[0] == 200:
                        mensagem = '200'
                        conexao.send(mensagem.encode())
                    else:
                        conexao.send("400;Algo deu errado :(".encode())

                # encerrando a conta
                if data[0]+data[1] == "06":
                    data = data.split(';')
                    retorno = self.encerrar_conta(data[1], data[2])
                    if retorno[0] == 200:
                        mensagem = str(retorno[0]) + ';' + retorno[1]
                        conexao.send(mensagem.encode())
                    else:
                        mensagem = str(retorno[0]) + ';' + retorno[1]
                        conexao.send(mensagem.encode())


                if data[0]+data[1] == "00":
                    self.mostrar_usuarios_banco()

            except ConnectionResetError:
                break

        conexao.close()
        print(f"> Conexão encerrada: {endereco}")


    def iniciar_banco(self):

        self.banco = sqlite3.connect('usuarios.db')

        # Cria uma tabela para armazenar os usuários (se ela não existir)
        self.banco.execute('''CREATE TABLE IF NOT EXISTS usuarios
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             NOME TEXT NOT NULL,
             EMAIL TEXT NOT NULL UNIQUE,
             SENHA TEXT NOT NULL,
             CPF TEXT NOT NULL UNIQUE);''')

        self.banco.execute('''CREATE TABLE IF NOT EXISTS conta_corrente
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
             ID_CLIENTE INTEGER,
             SALDO FLOAT NOT NULL,
             FOREIGN KEY(ID_CLIENTE) REFERENCES usuarios(ID));''')

        self.salvar_banco()
        self.encerrar_conexao_banco()
        

    def salvar_banco(self):
        self.banco.commit()


    def encerrar_conexao_banco(self):
        self.banco.close()

    def criar_usuario(self, nome, email, senha, cpf):
        try:
            self.banco = sqlite3.connect('usuarios.db')
            self.banco.execute('INSERT INTO usuarios (NOME, EMAIL, SENHA, CPF) VALUES (?, ?, ?, ?)', (nome, email, senha, cpf))

            id_usuario = self.banco.execute('SELECT ID FROM usuarios WHERE CPF = ?', (cpf,)).fetchone()[0]
            self.banco.execute('INSERT INTO conta_corrente (ID_CLIENTE, SALDO) VALUES (?, ?)', (id_usuario, 0))
            self.salvar_banco()
            self.encerrar_conexao_banco()
            return 200
        except:
            return 400


    def acessar_conta(self, email, senha):
        try:
            self.banco = sqlite3.connect('usuarios.db')
            cliente = self.banco.execute('SELECT * FROM usuarios WHERE EMAIL = ? AND SENHA = ?', (email, senha))
            for i in cliente:
                id_cliente = i[0]
                nome = i[1]
            id_conta_cliente = self.banco.execute('SELECT ID FROM conta_corrente WHERE ID_CLIENTE = ?', (id_cliente,)).fetchone()[0]
            self.salvar_banco()
            self.encerrar_conexao_banco()

            return [200, id_conta_cliente, nome, id_cliente]
        except:
            return (400, 'erro')

    def consultar_saldo(self, id_conta):
        try:
            self.banco = sqlite3.connect('usuarios.db')
            saldo = self.banco.execute('SELECT SALDO FROM conta_corrente WHERE ID = ?', (id_conta,)).fetchone()[0]
            self.salvar_banco()
            self.encerrar_conexao_banco()

            return [200, saldo]
        except:
            return (400, 'erro')
    
    def creditar_conta(self, id_conta, valor):
        try:
            self.banco = sqlite3.connect('usuarios.db')
            self.banco.execute('UPDATE conta_corrente SET SALDO = SALDO + ? WHERE ID = ?', (valor, id_conta))
            self.salvar_banco()
            self.encerrar_conexao_banco()

            return [200]
        except:
            return (400, 'erro')

    def debitar_conta(self, id_conta, valor):
        try:
            self.banco = sqlite3.connect('usuarios.db')
            self.banco.execute('UPDATE conta_corrente SET SALDO = SALDO - ? WHERE ID = ?', (valor, id_conta))
            self.salvar_banco()
            self.encerrar_conexao_banco()

            return [200]
        except:
            return (400, 'erro')

    def encerrar_conta(self, id_conta, id_cliente):
        # try:
        self.banco = sqlite3.connect('usuarios.db')
        saldo = self.banco.execute("SELECT SALDO FROM conta_corrente WHERE ID=?", (id_conta,)).fetchone()[0]
        if saldo == 0:
            self.banco.execute("DELETE FROM usuarios WHERE ID=?", (id_cliente,))
            self.banco.execute("DELETE FROM conta_corrente WHERE ID=?", (id_conta,))
            mensagem = "> Conta encerrada com sucesso!"
            codigo = 200
        else:
            mensagem = "> Conta não pode ser encerrada pois ainda possui saldo diferente de zero."
            codigo = 202
        self.salvar_banco()
        self.encerrar_conexao_banco()
        return [codigo, mensagem]
        # except:
        #     return (400, 'erro')


    def mostrar_usuarios_banco(self):
        self.banco = sqlite3.connect('usuarios.db')
        usuarios = self.banco.execute('SELECT * FROM usuarios')
        for usuario in usuarios:
            print(usuario)
        self.encerrar_conexao_banco()

    def start(self):
        while True:
            conexao, endereco = self.servidor.accept()
            thread = threading.Thread(target=self.gerenciar_cliente, args=(conexao, endereco))
            thread.start()

if __name__ == '__main__':
    server = Servidor('localhost', 6960)
    server.start()