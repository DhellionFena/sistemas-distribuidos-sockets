import socket
import os

class Cliente:

    def __init__(self, HOST, PORT):
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.HOST = HOST
        self.PORT = PORT
        self.conta_acessada = False
        
    
    def iniciar_conexao(self):
        self.cliente.connect((self.HOST, self.PORT))
    
    def testar_conexao(self):
        mensagem = "teste".encode()
        self.cliente.send(mensagem)
        data = self.cliente.recv(1024).decode()
        print(data)

    def encerrar_conexao(self):
        print("> Encerrando conexão")
        self.cliente.close()

    def criar_usuario(self):
        nome = input("> Insira seu nome:\n> ")
        email = input("> Insira seu email:\n> ")
        senha = input("> Insira seu senha:\n> ")
        cpf = input("> Insira seu cpf:\n> ")
        mensagem = "02;"+ nome + ";" + email + ";" + senha + ";" + cpf
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        print("> " + data)

    def acessar_conta(self):
        email = input("> Insira seu email:\n> ")
        senha = input("> Insira seu senha:\n> ")
        mensagem = "01;" + email + ";" + senha
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        data = data.split(';')
        if (data[0] == '200'):
            self.conta_acessada = True
            self.id_conta = data[1]
            self.nome = data[2]
            self.id_cliente = data[3]
        else:
            print("> Algum erro aconteceu.")

    def consultar_saldo(self):
        mensagem = "03;" + self.id_conta
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        data = data.split(';')
        if (data[0] == '200'):
            print("> Seu Saldo é de: R$" + data[1])
            self.saldo = data[1]
        else:
            print("> Algum erro aconteceu.")

    def creditar_saldo(self):
        valor = float(input("> Insira o valor que deseja creditar:\n> R$"))
        mensagem = "04;" + self.id_conta + ";" + str(valor)
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        data = data.split(';')
        if (data[0] == '200'):
            print("> Valor creditado com sucesso!")
        else:
            print("> Algum erro aconteceu.")

    def debitar_saldo(self):
        valor = float(input("> Insira o valor que deseja debitar:\n> R$"))
        mensagem = "05;" + self.id_conta + ";" + str(valor)
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        data = data.split(';')
        if (data[0] == '200'):
            print("> Valor debitado com sucesso!")
        else:
            print("> Algum erro aconteceu.")

    def encerrar_conta(self):
        mensagem = "06;" + self.id_conta + ";" + self.id_cliente
        self.cliente.send(mensagem.encode())
        data = self.cliente.recv(1024).decode()
        data = data.split(';')
        if (data[0] == '200'):
            print(data[1])
            self.conta_acessada = False
        else:
            print("> Algum erro aconteceu.")

    
    def start(self):
        # PRINTAR TODAS AS OPCOES DO CLIENTE E MANTER DENTRO DE UM LOOP TIPO UM MENU
        self.iniciar_conexao()

        while True:
            os.system("cls")
            if not self.conta_acessada:
                print("> Escolha as opções:")
                print("[1] Acessar Conta")
                print("[2] Criar Conta")
                print("[0] Finalizar Conexão")
                resposta = int(input("> "))

                if resposta == 69:
                    self.testar_conexao()
                    os.system("pause")
                elif resposta == 1:
                    self.acessar_conta()
                    os.system("pause")
                elif resposta == 2:
                    self.criar_usuario()
                    os.system("pause")
                elif resposta == 3:
                    self.cliente.send("00".encode())
                    os.system("pause")
                elif resposta == 0:
                    self.encerrar_conexao()
                    break
                else:
                    print("> Opção Inválida!")
                    os.system("pause")
            else:
                print("> Olá " + self.nome + "! O que deseja fazer?")
                print("[1] Creditar Conta")
                print("[2] Debitar Conta")
                print("[3] Acessar Saldo")
                print("[4] Encerrar Conta")
                print("[0] Finalizar Conexão")
                resposta = int(input("> "))

                if resposta == 1:
                    self.creditar_saldo()
                    os.system("pause")
                elif resposta == 2:
                    self.debitar_saldo()
                    os.system("pause")
                elif resposta == 3:
                    self.consultar_saldo()
                    os.system("pause")
                elif resposta == 4:
                    self.encerrar_conta()
                    os.system("pause")
                elif resposta == 0:
                    self.encerrar_conexao()
                    break
                else:
                    print("> Opção Inválida!")
                    os.system("pause")



if __name__ == '__main__':
    cliente = Cliente('localhost', 6960)
    cliente.start()
