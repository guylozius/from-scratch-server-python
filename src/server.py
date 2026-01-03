import socket
def create_server_socket():
    host = socket.gethostname()
    port = 8080
    #Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    #Bind the socket to the address and port
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr} has been established!")
    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break
        client_socket.sendall(data.encode('utf-8'))
    client_socket.close()
    server_socket.close()

