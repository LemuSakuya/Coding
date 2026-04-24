import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8080))
server_socket.listen(1)

print("Server is listening on port 8080")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established")
    client_socket.send(b"Welcome to the server!")
    client_socket.close()