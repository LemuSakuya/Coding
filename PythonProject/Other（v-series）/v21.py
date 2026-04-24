import socket


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8080))

message = client_socket.recv(1024)
print(message.decode())  # 输出: Welcome to the server!

client_socket.close()