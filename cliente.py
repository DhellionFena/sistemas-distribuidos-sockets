import socket

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(('localhost', 6969))

mensagem = "racobaldo".encode()
cliente.send(mensagem)

data = cliente.recv(1024).decode()
print(data)
cliente.close()