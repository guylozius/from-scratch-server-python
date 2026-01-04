import socket
import time

def create_server_socket():
    host = "0.0.0.0"   # or "127.0.0.1" for local only
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(1)

    server_socket.settimeout(10.0)  # ✅ set once

    print(f"Server listening on {host}:{port}")

    shutdown = False
    last_log_time = 0

    while not shutdown:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr} has been established!")

            client_socket.settimeout(10.0)

            try:
                data = client_socket.recv(1024)
                if not data:
                    print("No data received. Closing connection.")
                else:
                    text = data.decode("utf-8", errors="replace")
                    print(f"Received data: {text}")
                    client_socket.sendall(data)  # echo back raw bytes

            except socket.timeout:
                print("Client timed out. Closing connection.")

            finally:
                try:
                    client_socket.sendall(b"Closing connection.\n")
                except Exception:
                    pass
                client_socket.close()

        except socket.timeout:
            current_time = time.time()
            if current_time - last_log_time >= 5:
                print("No incoming connections. Continuing to listen...")
                last_log_time = current_time
            continue

        except KeyboardInterrupt:
            print("Server is shutting down.")
            shutdown = True

    server_socket.close()
    print("Server stopped.")
